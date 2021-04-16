from datetime import datetime
from importlib import import_module
import inspect
import json
import logging
from multiprocessing import Process
from psycopg2.extras import execute_batch
import sys
import time

from django.conf import settings
from django.contrib.admin.utils import quote
from django.contrib.auth.models import AbstractUser, Group
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied
from django.core import mail
from django.core.validators import FileExtensionValidator
from django.db import models, DEFAULT_DB_ALIAS, connections, transaction
from django.db.models import Q
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver
from django import forms
from django.forms.models import modelform_factory
from django.urls import NoReverseMatch, reverse
from django.utils import timezone
from django.utils.encoding import force_text
from django.utils.html import mark_safe, escape
from django.utils.translation import gettext_lazy as _
from django.utils.text import capfirst

from .fields import JSONBField
from .. import runFunction

logger = logging.getLogger(__name__)


class HierarchyModel(models.Model):
    lft = models.PositiveIntegerField(
        db_index=True, editable=False, null=True, blank=True
    )
    rght = models.PositiveIntegerField(null=True, editable=False, blank=True)
    lvl = models.PositiveIntegerField(null=True, editable=False, blank=True)
    name = models.CharField(
        _("name"), max_length=300, primary_key=True, help_text=_("Unique identifier")
    )
    owner = models.ForeignKey(
        "self",
        verbose_name=_("owner"),
        null=True,
        blank=True,
        related_name="xchildren",
        help_text=_("Hierarchical parent"),
        on_delete=models.SET_NULL,
    )

    def save(self, *args, **kwargs):
        # Trigger recalculation of the hieracrhy.
        # TODO this triggers the recalculation in too many cases, including a lot
        # of changes which don't require it. Alternative solution is to use the
        # pre-save signal which has more information.
        self.lft = None
        self.rght = None
        self.lvl = None

        # Call the real save() method
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        try:
            # Update an arbitrary other object to trigger recalculation of the hierarchy
            obj = self.__class__.objects.using(self._state.db).exclude(pk=self.pk)[0]
            obj.lft = None
            obj.rght = None
            obj.lvl = None
            obj.save(update_fields=["lft", "rght", "lvl"], using=self._state.db)
        except Exception:
            # Failure can happen when eg we delete the last record
            pass
        # Call the real delete() method
        super().delete(*args, **kwargs)

    class Meta:
        abstract = True

    @classmethod
    def rebuildHierarchy(cls, database=DEFAULT_DB_ALIAS):

        # Verify whether we need to rebuild or not.
        # We search for the first record whose lft field is null.
        if len(cls.objects.using(database).filter(lft__isnull=True)[:1]) == 0:
            return

        nodes = {}
        children = {}
        updates = []

        def tagChildren(me, left, level):
            right = left + 1
            # Get all children of this node
            for i in children.get(me, []):
                # Recursive execution of this function for each child of this node
                right = tagChildren(i, right, level + 1)

            # After processing the children of this node now know its left and right values
            updates.append((left, right, level, me))

            # Remove from node list (to mark as processed)
            del nodes[me]

            # Return the right value of this node + 1
            return right + 1

        # Load all nodes in memory
        for i in cls.objects.using(database).values("name", "owner"):
            if i["name"] == i["owner"]:
                logging.error("Data error: '%s' points to itself as owner" % i["name"])
                nodes[i["name"]] = None
            else:
                nodes[i["name"]] = i["owner"]
                if i["owner"]:
                    if not i["owner"] in children:
                        children[i["owner"]] = set()
                    children[i["owner"]].add(i["name"])
        keys = sorted(nodes.items())

        # Loop over nodes without parent
        cnt = 1
        for i, j in keys:
            if j is None:
                cnt = tagChildren(i, cnt, 0)

        if nodes:
            # If the nodes dictionary isn't empty, it is an indication of an
            # invalid hierarchy.
            # There are loops in your hierarchy, ie parent-chains not ending
            # at a top-level node without parent.
            bad = nodes.copy()
            updated = True
            while updated:
                updated = False
                for i in bad.keys():
                    ok = True
                    for j, k in bad.items():
                        if k == i:
                            ok = False
                            break
                    if ok:
                        # If none of the bad keys points to me as a parent, I am unguilty
                        del bad[i]
                        updated = True
            logging.error("Data error: Hierarchy loops among %s" % sorted(bad.keys()))
            for i, j in sorted(bad.items()):
                children[j].remove(i)
                nodes[i] = None

            # Continue loop over nodes without parent
            keys = sorted(nodes.items())
            for i, j in keys:
                if j is None:
                    cnt = tagChildren(i, cnt, 0)

        # Write all results to the database
        with transaction.atomic(using=database):
            cursor = connections[database].cursor()
            execute_batch(
                cursor,
                "update %s set lft=%%s, rght=%%s, lvl=%%s where name = %%s"
                % connections[database].ops.quote_name(cls._meta.db_table),
                updates,
            )

    @classmethod
    def createRootObject(cls, database=DEFAULT_DB_ALIAS):
        """
        Rebuilds the hierarchy, and also assures we only have a single root object
        """
        # Rebuild hierarchy
        cls.rebuildHierarchy(database=database)

        # Create root
        roots = cls.objects.using(database).filter(lvl=0).count()
        if roots != 1:
            # create a 'All dimensions' item (that might already be there)
            rootname = "All %ss" % cls._meta.db_table
            obj, created = cls.objects.using(database).get_or_create(name=rootname)
            if created:
                obj.description = "Automatically created root object"
                obj.save()
            else:
                # This is to force hierarchy rebuild that may not occur as all lft values are populated.
                obj.lft = None
                obj.save(update_fields=["lft"])
            cls.objects.using(database).filter(owner__isnull=True).exclude(
                name=rootname
            ).update(owner=obj)

            # Rebuild the hierarchy again with the new root
            cls.rebuildHierarchy(database=database)


class MultiDBManager(models.Manager):
    def get_queryset(self):
        from .middleware import _thread_locals

        req = getattr(_thread_locals, "request", None)
        if req:
            return (
                super().get_queryset().using(getattr(req, "database", DEFAULT_DB_ALIAS))
            )
        else:
            db = getattr(_thread_locals, "database", None)
            return super().get_queryset().using(db or DEFAULT_DB_ALIAS)


class MultiDBRouter:
    def db_for_read(self, model, **hints):
        from .middleware import _thread_locals

        req = getattr(_thread_locals, "request", None)
        if req:
            return getattr(req, "database", None)
        else:
            return getattr(_thread_locals, "database", None)

    def db_for_write(self, model, **hints):
        from .middleware import _thread_locals

        req = getattr(_thread_locals, "request", None)
        if req:
            return getattr(req, "database", None)
        else:
            return getattr(_thread_locals, "database", None)


class AuditModel(models.Model):
    """
    This is an abstract base model.
    It implements the capability to maintain:
    - the date of the last modification of the record.
    - a string intended to describe the source system that supplied the record
    """

    # Database fields
    source = models.CharField(
        _("source"), db_index=True, max_length=300, null=True, blank=True
    )
    lastmodified = models.DateTimeField(
        _("last modified"), editable=False, db_index=True, default=timezone.now
    )

    objects = MultiDBManager()  # The default manager.

    def save(self, *args, **kwargs):
        # Update the field with every change
        self.lastmodified = datetime.now()

        # Call the real save() method
        super().save(*args, **kwargs)

    class Meta:
        abstract = True


class Parameter(AuditModel):
    # Database fields
    name = models.CharField(_("name"), max_length=60, primary_key=True)
    value = models.CharField(_("value"), max_length=1000, null=True, blank=True)
    description = models.CharField(
        _("description"), max_length=1000, null=True, blank=True
    )

    def __str__(self):
        return self.name

    class Meta(AuditModel.Meta):
        db_table = "common_parameter"
        verbose_name = _("parameter")
        verbose_name_plural = _("parameters")

    @staticmethod
    def getValue(key, database=DEFAULT_DB_ALIAS, default=None):
        try:
            return Parameter.objects.using(database).only("value").get(pk=key).value
        except Exception:
            return default


class Scenario(models.Model):
    scenarioStatus = (("free", _("free")), ("in use", _("in use")), ("busy", _("busy")))

    # Database fields
    name = models.CharField(_("name"), max_length=300, primary_key=True)
    description = models.CharField(
        _("description"), max_length=500, null=True, blank=True
    )
    status = models.CharField(
        _("status"), max_length=10, null=False, blank=False, choices=scenarioStatus
    )
    lastrefresh = models.DateTimeField(_("last refreshed"), null=True, editable=False)
    help_url = models.URLField("help", null=True, editable=False)

    def __str__(self):
        return self.name

    @staticmethod
    def syncWithSettings():
        try:
            # Bring the scenario table in sync with settings.databases
            with transaction.atomic(savepoint=False):
                dbs = [i for i, j in settings.DATABASES.items() if j["NAME"]]
                scs = []
                for sc in Scenario.objects.using(DEFAULT_DB_ALIAS):
                    if sc.name not in dbs:
                        sc.delete()
                    else:
                        scs.append(sc.name)
                for db in dbs:
                    if db not in scs:
                        if db == DEFAULT_DB_ALIAS:
                            Scenario(
                                name=db, status="In use", description="Production"
                            ).save(using=DEFAULT_DB_ALIAS)
                        else:
                            Scenario(name=db, status="Free").save(
                                using=DEFAULT_DB_ALIAS
                            )
        except Exception:
            # Failures are acceptable - eg when the default database has not been intialized yet
            pass

    def __lt__(self, other):
        # Default database is always first in the list
        if self.name == DEFAULT_DB_ALIAS:
            return True
        elif other.name == DEFAULT_DB_ALIAS:
            return False
        # Other databases are sorted by their description
        return (self.description or self.name) < (other.description or other.name)

    class Meta:
        db_table = "common_scenario"
        default_permissions = ("copy", "release", "promote")
        verbose_name_plural = _("scenarios")
        verbose_name = _("scenario")
        ordering = ["name"]


class User(AbstractUser):
    languageList = tuple(
        [("auto", _("Detect automatically"))] + list(settings.LANGUAGES)
    )
    language = models.CharField(
        _("language"), max_length=10, choices=languageList, default="auto"
    )
    theme = models.CharField(
        _("theme"),
        max_length=20,
        default=settings.DEFAULT_THEME,
        choices=[(i, capfirst(i)) for i in settings.THEMES],
    )
    pagesize = models.PositiveIntegerField(
        _("page size"), default=settings.DEFAULT_PAGESIZE
    )
    horizonbuckets = models.CharField(max_length=300, blank=True, null=True)
    horizonstart = models.DateTimeField(blank=True, null=True)
    horizonend = models.DateTimeField(blank=True, null=True)
    horizontype = models.BooleanField(blank=True, default=True)
    horizonlength = models.IntegerField(blank=True, default=6, null=True)
    horizonbefore = models.IntegerField(blank=True, default=0, null=True)
    horizonunit = models.CharField(
        blank=True,
        max_length=5,
        default="month",
        null=True,
        choices=(("day", "day"), ("week", "week"), ("month", "month")),
    )
    avatar = models.ImageField(null=True, blank=True)
    lastmodified = models.DateTimeField(
        _("last modified"),
        auto_now=True,
        null=True,
        blank=True,
        editable=False,
        db_index=True,
    )

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        """
        Every change to a user model is saved to all active scenarios.

        The is_superuser and is_active fields can be different in each scenario.
        All other fields are expected to be identical in each database.

        Because of the logic in this method creating users directly in the
        database tables is NOT a good idea!
        """
        # We want to automatically give access to the django admin to all users
        self.is_staff = True
        if not using:
            using = getattr(self, "_state", None)
            if using:
                using = using.db
            else:
                from .middleware import _thread_locals

                using = getattr(_thread_locals, "database", DEFAULT_DB_ALIAS)

        scenarios = [
            i["name"]
            for i in Scenario.objects.using(DEFAULT_DB_ALIAS)
            .filter(status="In use")
            .values("name")
            if i["name"] in settings.DATABASES
        ]

        # The same id of a new user MUST be identical in all databases.
        # We manipulate the sequences, and correct if required.
        newuser = False
        tmp_is_active = self.is_active
        tmp_is_superuser = self.is_superuser
        if self.id is None:
            newuser = True
            self.id = 0
            cur_seq = {}
            for db in scenarios:
                cursor = connections[db].cursor()
                cursor.execute("select nextval('common_user_id_seq')")
                cur_seq[db] = cursor.fetchone()[0]
                if cur_seq[db] > self.id:
                    self.id = cur_seq[db]
            for db in scenarios:
                if cur_seq[db] != self.id:
                    cursor = connections[db].cursor()
                    cursor.execute(
                        "select setval('common_user_id_seq', %s)", [self.id - 1]
                    )
            self.is_active = False
            self.is_superuser = False

        # Save only specific fields which we want to have identical across
        # all scenario databases.
        if not update_fields:
            update_fields2 = [
                "username",
                "password",
                "last_login",
                "first_name",
                "last_name",
                "email",
                "date_joined",
                "language",
                "theme",
                "avatar",
                "pagesize",
                "horizonlength",
                "horizontype",
                "horizonbuckets",
                "horizonstart",
                "horizonend",
                "horizonunit",
                "lastmodified",
                "is_staff",
            ]
        else:
            # Important is NOT to save the is_active and is_superuser fields.
            update_fields2 = update_fields[:]  # Copy!
            if "is_active" in update_fields2:
                update_fields2.remove("is_active")
            if "is_superuser" in update_fields:
                update_fields2.remove("is_superuser")
        if update_fields2 or newuser:
            for db in scenarios:
                if db == using:
                    continue
                try:
                    with transaction.atomic(using=db, savepoint=True):
                        super().save(
                            force_insert=force_insert,
                            force_update=force_update,
                            using=db,
                            update_fields=update_fields2 if not newuser else None,
                        )
                except Exception:
                    try:
                        with transaction.atomic(using=db, savepoint=False):
                            newuser = True
                            self.is_active = False
                            self.is_superuser = False
                            super().save(
                                force_insert=force_insert,
                                force_update=force_update,
                                using=db,
                            )
                            if settings.DEFAULT_USER_GROUP:
                                grp = (
                                    Group.objects.all()
                                    .using(db)
                                    .get_or_create(name=settings.DEFAULT_USER_GROUP)[0]
                                )
                                self.groups.add(grp.id)
                    except Exception as e:
                        logger.warning(
                            "Can't save user '%s' in scenario '%s': %s"
                            % (self.username, db, e)
                        )

        # Continue with the regular save, as if nothing happened.
        self.is_active = tmp_is_active
        self.is_superuser = tmp_is_superuser
        usr = super().save(
            force_insert=force_insert,
            force_update=force_update,
            using=using,
            update_fields=update_fields,
        )
        if settings.DEFAULT_USER_GROUP and newuser:
            grp = (
                Group.objects.all()
                .using(using)
                .get_or_create(name=settings.DEFAULT_USER_GROUP)[0]
            )
            self.groups.add(grp.id)
        return usr

    def joined_age(self):
        """
        Returns the number of days since the user joined
        """
        if self.date_joined.year == 2000:
            # This is the user join date from the demo database.
            # We'll consider that a new user.
            self.date_joined = self.last_login
            self.save()
        return (datetime.now() - self.date_joined).total_seconds() / 86400

    class Meta:
        db_table = "common_user"
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def getPreference(self, prop, default=None, database=DEFAULT_DB_ALIAS):
        try:
            result = None
            for p in (
                UserPreference.objects.all()
                .using(database)
                .filter(property=prop)
                .filter(Q(user__isnull=True) | Q(user=self.id))
                .order_by("-user")
                .only("user", "value")
            ):
                if result:
                    result.update(p.value)
                else:
                    result = p.value
            return result if result else default
        except ValueError:
            logger.error("Invalid preference '%s' of user '%s'" % (prop, self.username))
            return default
        except Exception:
            return default

    def setPreference(self, prop, val, database=DEFAULT_DB_ALIAS):
        if val is None:
            if prop in settings.GLOBAL_PREFERENCES and self.is_superuser:
                # Delete global preferences
                UserPreference.objects.all().using(database).filter(
                    user__isnull=True, property=prop
                ).delete()
            # Delete user preferences
            self.preferences.using(database).filter(user=self, property=prop).delete()
        else:
            sql = """
                insert into common_preference
                (user_id, property, value)
                values (%s, %s, %s)
                on conflict (user_id, property)
                do update set value = %s
                """
            with connections[database].cursor() as cursor:
                if prop in settings.GLOBAL_PREFERENCES:
                    val_global = {
                        k: v
                        for k, v in val.items()
                        if k in settings.GLOBAL_PREFERENCES[prop]
                    }
                    val_user = {
                        k: v
                        for k, v in val.items()
                        if k not in settings.GLOBAL_PREFERENCES[prop]
                    }
                    if val_global and self.is_superuser:
                        # A superuser can save global preferences for this property
                        # Note: the on conflict clause in the insert sql doesn't prevent
                        # duplicates to be inserted since the user_id is null.
                        cursor.execute(
                            """
                            delete from common_preference
                            where user_id is null and property = %s
                            """,
                            [prop],
                        )
                        t = json.dumps(val_global)
                        cursor.execute(sql, [None, prop, t, t])
                    if val_user:
                        # Everyone can save his personal preferences for this property
                        t = json.dumps(val_user)
                        cursor.execute(sql, [self.id, prop, t, t])
                else:
                    # No global preferences configured for this property
                    t = json.dumps(val)
                    cursor.execute(sql, (self.id, prop, t, t))


class UserPreference(models.Model):
    class UserPreferenceManager(models.Manager):
        def get_by_natural_key(self, usr, prop):
            return self.get(user=usr, property=prop)

    objects = UserPreferenceManager()

    id = models.AutoField(_("identifier"), primary_key=True)
    user = models.ForeignKey(
        User,
        verbose_name=_("user"),
        blank=False,
        null=True,
        editable=False,
        related_name="preferences",
        on_delete=models.CASCADE,
    )
    property = models.CharField(max_length=100, blank=False, null=False)
    value = JSONBField(max_length=1000, blank=False, null=False)

    def natural_key(self):
        return (self.user, self.property)

    class Meta:
        db_table = "common_preference"
        unique_together = (("user", "property"),)
        verbose_name = "preference"
        verbose_name_plural = "preferences"
        default_permissions = []


@receiver(pre_delete, sender=User)
def delete_user(sender, instance, **kwargs):
    raise PermissionDenied


class Comment(models.Model):
    type_list = (
        ("add", _("Add")),
        ("change", _("Change")),
        ("delete", _("Delete")),
        ("comment", _("comment")),
        ("follower", _("follower")),
    )
    id = models.AutoField(_("identifier"), primary_key=True)
    type = models.CharField(
        _("type"), max_length=10, null=False, default="add", choices=type_list
    )
    content_type = models.ForeignKey(
        ContentType,
        verbose_name=_("content type"),
        related_name="content_type_set_for_%(class)s",
        on_delete=models.CASCADE,
    )
    object_repr = models.CharField(_("object repr"), max_length=200)
    object_pk = models.TextField(_("object id"))
    content_object = GenericForeignKey(ct_field="content_type", fk_field="object_pk")
    comment = models.TextField(_("message"), max_length=3000)
    attachment = models.FileField(
        null=True,
        blank=True,
        validators=[
            FileExtensionValidator(
                allowed_extensions=[
                    ext[1:] for ext in settings.MEDIA_EXTENSIONS.split(",")
                ]
            )
        ],
    )
    user = models.ForeignKey(
        User,
        verbose_name=_("user"),
        blank=True,
        null=True,
        editable=False,
        on_delete=models.SET_NULL,
    )
    lastmodified = models.DateTimeField(
        _("last modified"), default=timezone.now, editable=False, db_index=True
    )
    processed = models.BooleanField("processed", default=False, db_index=True)

    def model_name(self):
        m = self.content_type.model_class()
        return "%s.%s" % (m._meta.app_label, m._meta.model_name)

    def safe(self):
        return self.content_type.model_class() == SystemMessage

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        from .middleware import _thread_locals

        if not using:
            using = getattr(self, "_state", None)
            if using:
                using = using.db
            else:
                using = getattr(_thread_locals, "database", DEFAULT_DB_ALIAS)
        tmp = super().save(
            force_insert=force_insert,
            force_update=force_update,
            using=using,
            update_fields=update_fields,
        )
        if update_fields != ["processed"]:
            req = getattr(_thread_locals, "request", None)
            NotificationFactory.launchWorker(
                database=using,
                url="%s://%s" % ("https" if req.is_secure() else "http", req.get_host())
                if req
                else None,
            )
        return tmp

    def attachmentlink(self):
        if self.attachment:
            return mark_safe(
                '<a href="%s" style="text-decoration:underline">.%s&nbsp;<i class="fa fa-2x fa-paperclip"></i></a>'
                % (self.attachment.url, self.attachment.url.split(".")[-1].lower())
            )
        else:
            return ""

    def getURL(self, database=DEFAULT_DB_ALIAS):
        if database == DEFAULT_DB_ALIAS:
            return "/detail/%s/%s/%s/" % (
                self.content_type.app_label,
                self.content_type.model,
                quote(self.object_pk),
            )
        else:
            return "%s/detail/%s/%s/%s/" % (
                database,
                self.content_type.app_label,
                self.content_type.model,
                quote(self.object_pk),
            )

    class Meta:
        db_table = "common_comment"
        ordering = ("id",)
        verbose_name = _("comment")
        verbose_name_plural = _("comments")
        default_permissions = []

    def __str__(self):
        return "%s: %s..." % (self.object_pk, self.comment[:50])

    def get_admin_url(self):
        """
        Returns the admin URL to edit the object represented by this comment.
        """
        if self.content_type and self.object_pk:
            url_name = "data:%s_%s_change" % (
                self.content_type.app_label,
                self.content_type.model,
            )
            try:
                return reverse(url_name, args=(quote(self.object_pk),))
            except NoReverseMatch:
                try:
                    url_name = "admin:%s_%s_change" % (
                        self.content_type.app_label,
                        self.content_type.model,
                    )
                    return reverse(url_name, args=(quote(self.object_pk),))
                except NoReverseMatch:
                    pass
        return None

    def getMail(self, url=None, database=DEFAULT_DB_ALIAS):
        """
        Returns a tuple (subject, body_text, body_html) for an email about this message.
        """
        body_text = "%s --- %s" % (url, self.comment)
        if url:
            body_html = [
                """
                <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
                <html>
                <head>
                <meta http-equiv="content-type" content="text/html; charset=utf-8">
                </head>
                <body>
                """
            ]
            if self.type != "delete":
                body_html.append(
                    "<button><a href='%s%s%s'>View</a></button><br><br>"
                    % (
                        url,
                        "/%s" % database if database != DEFAULT_DB_ALIAS else "",
                        self.getURL(),
                    )
                )
            if self.attachment:
                body_html.append(
                    "<a href='%s%s'>View attachment</a><br><br>"
                    % (url, self.attachment.url)
                )
            body_html.append("%s<br></body></html>" % escape(self.comment))
        else:
            body_html = None
        if self.type == "add":
            return (
                "frePPLe: Added %s '%s'" % (self.content_type.model, self.object_repr),
                body_text,
                "".join(body_html) if body_html else None,
            )
        elif self.type == "change":
            return (
                "frePPLe: Changed %s '%s'"
                % (self.content_type.model, self.object_repr),
                body_text,
                "".join(body_html) if body_html else None,
            )
        elif self.type == "delete":
            return (
                "frePPLe: Deleted %s '%s'"
                % (self.content_type.model, self.object_repr),
                body_text,
                "".join(body_html) if body_html else None,
            )
        elif self.type == "comment":
            return (
                "frePPLe: New comment on %s '%s'"
                % (self.content_type.model, self.object_repr),
                body_text,
                "".join(body_html) if body_html else None,
            )
        else:
            return (
                "frePPLe: %s %s" % (self.content_type.model, self.object_repr),
                body_text,
                body_html,
            )


class SystemMessage(models.Model):
    """
    A dummy model without database table.
    It is used to publish system notifications to users.
    """

    class Meta:
        managed = False
        default_permissions = ()

    @classmethod
    def add(cls, msg, database=None):
        if database:
            scenarios = [database]
        else:
            scenarios = [
                i["name"]
                for i in Scenario.objects.using(DEFAULT_DB_ALIAS)
                .filter(status="In use")
                .values("name")
                if i["name"] in settings.DATABASES
            ]
        for db in scenarios:
            c = Comment(
                type="comment",
                content_type=ContentType.objects.using(db).get(
                    app_label="common", model="systemmessage"
                ),
                object_pk="",
                object_repr="",
                comment=msg,
                user=User.objects.using(db).get(username="admin"),
                processed=True,
            )
            c.save(using=db)
            for u in User.objects.all().using(db):
                Notification(comment=c, user=u).save(using=db)


class Follower(models.Model):
    type_list = (("M", "email"), ("O", "online"))

    id = models.AutoField(_("identifier"), primary_key=True)
    content_type = models.ForeignKey(
        ContentType, verbose_name=_("model name"), on_delete=models.CASCADE
    )
    object_pk = models.TextField(_("object name"), null=True)
    content_object = GenericForeignKey(ct_field="content_type", fk_field="object_pk")
    user = models.ForeignKey(
        User, verbose_name=_("user"), blank=True, on_delete=models.CASCADE
    )
    type = models.CharField(
        _("type"), max_length=10, null=False, default="O", choices=type_list
    )
    args = JSONBField(blank=True, null=True)

    def getURL(self, database=DEFAULT_DB_ALIAS):
        if database == DEFAULT_DB_ALIAS:
            return "/detail/%s/%s/%s/" % (
                self.content_type.app_label,
                self.content_type.model,
                quote(self.object_pk),
            )
        else:
            return "%s/detail/%s/%s/%s/" % (
                database,
                self.content_type.app_label,
                self.content_type.model,
                quote(self.object_pk),
            )

    @classmethod
    def xxxgetModelForm(cls, fields, database=DEFAULT_DB_ALIAS):
        template = modelform_factory(
            cls,
            fields=fields,
            # formfield_callback=lambda f: (
            #    isinstance(f, RelatedField) and f.formfield(using=database)
            # )
            # or f.formfield(),
        )

        class FollowerForm(template):
            content_type = forms.CharField() if "resource" in fields else None

            def clean(self):
                try:
                    self.data = self.data.items()
                    self.data["content_type"] = ContentType.objects.get(
                        model=self.data["content_type"]
                    ).pk
                except Exception as e:
                    print(e)
                    raise forms.ValidationError("Invalid content type")
                return super().clean()

        return FollowerForm

    def clean(self):
        from .middleware import _thread_locals

        request = getattr(_thread_locals, "request", None)
        if request and request.user:
            self.user = request.user

    class Meta:
        verbose_name = _("follower")
        verbose_name_plural = _("followers")
        db_table = "common_follower"
        default_permissions = ()


class Notification(models.Model):
    type_list = (("M", "email"), ("O", "online"))
    status_list = (("U", "unread"), ("R", "read"))

    id = models.AutoField(_("identifier"), primary_key=True)
    comment = models.ForeignKey(
        Comment, verbose_name=_("comment"), on_delete=models.CASCADE, null=True
    )
    user = models.ForeignKey(User, verbose_name=_("user"), on_delete=models.CASCADE)
    status = models.CharField(
        _("status"), max_length=5, null=False, default="U", choices=status_list
    )
    type = models.CharField(
        _("type"), max_length=5, null=False, default="O", choices=type_list
    )
    follower = models.ForeignKey(
        Follower, verbose_name=_("follower"), null=True, on_delete=models.SET_NULL
    )

    def clean(self):
        from .middleware import _thread_locals

        request = getattr(_thread_locals, "request", None)
        if request and request.user:
            self.user = request.user

    def __str__(self):
        return "%s: %s" % (self.user.username, self.comment)

    @classmethod
    def wait(cls):
        NotificationFactory.join()

    class Meta:
        verbose_name = _("notification")
        verbose_name_plural = _("notifications")
        db_table = "common_notification"


class NotificationFactory:
    _workers = {}
    _reg = {}

    @classmethod
    def launchWorker(cls, database=DEFAULT_DB_ALIAS, url=None):
        worker = cls._workers.get(database, None)
        if worker and not worker.is_alive():
            worker = None
            del NotificationFactory._workers[database]
        if not worker:
            p = Process(
                target=runFunction,
                args=["data_admin.common.models.NotificationFactory"],
                kwargs={"url": url, "database": database},
                daemon=True,
            )
            cls._workers[database] = p
            p.start()

    @classmethod
    def register(cls, followerclass, messageclasses):
        def decorator(func):
            if not inspect.isclass(followerclass):
                raise Exception("NotificationFactory needs a class as first argument")
            for m in messageclasses:
                if not inspect.isclass(m):
                    raise Exception(
                        "NotificationFactory needs a class list as second argument"
                    )
                if m in cls._reg:
                    cls._reg[m].append(func)
                else:
                    cls._reg[m] = [func]
            func.messages = messageclasses
            func.follower = followerclass
            return func

        return decorator

    @classmethod
    def _buildRegistry(cls):
        # Find all notification registrations
        if cls._reg:
            return
        for app in reversed(settings.INSTALLED_APPS):
            try:
                import_module("%s.notifications" % app)
            except ImportError as e:
                # Silently ignore if it's the commands module which isn't found
                if str(e) not in (
                    "No module named %s.notifications" % app,
                    "No module named '%s.notifications'" % app,
                ):
                    raise e

    @classmethod
    def start(cls, url=None, database=DEFAULT_DB_ALIAS):
        """
        Every server process will have at most 1 worker processes for each database.
        The worker process is spawned by the multiprocessing module and runs this method.
        """
        cls._buildRegistry()
        try:
            from .middleware import _thread_locals

            setattr(_thread_locals, "database", database)
            followers = list(
                Follower.objects.all()
                .using(database)
                .filter(user__is_active=True)
                .order_by("id")
            )
            idle_loop_done = False
            while True:
                with transaction.atomic(using=database):
                    empty = True
                    emails = []
                    if followers:
                        for msg in (
                            Comment.objects.all()
                            .using(database)
                            .filter(processed=False)
                            .order_by("id")
                            .select_related("content_type")
                            .select_for_update(skip_locked=True, of=("self",))[:50]
                        ):
                            empty = False
                            recipients = set()
                            try:
                                created = set()
                                model = msg.content_type.model_class()
                                view_permission = (
                                    "%s.view_%s"
                                    % (model._meta.app_label, model._meta.model_name)
                                    if "view" in model._meta.default_permissions
                                    else None
                                )
                                meta = cls._reg.get(model, None)
                                if meta:
                                    for flw in followers:
                                        for c in meta:
                                            try:
                                                if (
                                                    flw.user not in created
                                                    and flw.content_type.model_class()
                                                    in c.messages
                                                    and (
                                                        flw.object_pk == "all"
                                                        or c(flw, msg)
                                                    )
                                                    and (
                                                        not view_permission
                                                        or flw.user.has_perm(
                                                            view_permission
                                                        )
                                                    )
                                                ):
                                                    Notification(
                                                        comment=msg,
                                                        user=flw.user,
                                                        type=flw.type,
                                                        follower=flw,
                                                    ).save(database)
                                                    if (
                                                        flw.type == "M"
                                                        and flw.user.email
                                                        and settings.EMAIL_HOST
                                                    ):
                                                        recipients.add(flw.user.email)
                                                    created.add(flw.user)
                                                    break
                                            except Exception as e:
                                                logger.error(
                                                    "Exception in notification function %s: %s"
                                                    % (c, e)
                                                )
                                msg.processed = True
                                msg.save(update_fields=["processed"], using=database)
                                if recipients:
                                    data = msg.getMail(url, database)
                                    email = mail.EmailMultiAlternatives(
                                        data[0],
                                        data[1],
                                        settings.DEFAULT_FROM_EMAIL,
                                        recipients,
                                    )
                                    if data[2]:
                                        email.attach_alternative(data[2], "text/html")
                                    emails.append(email)
                            except Exception as e:
                                logger.error(
                                    "Couldn't create nofications for message %s: %s"
                                    % (msg.id, e)
                                )
                        if emails:
                            connection = None
                            try:
                                connection = mail.get_connection()
                                connection.open()
                                connection.send_messages(emails)
                            except Exception as e:
                                logger.error("Error mailing messages: %s" % e)
                            finally:
                                if connection:
                                    connection.close()
                    else:
                        # No followers at all -> All messages can immediately be marked processed
                        recs = (
                            Comment.objects.all()
                            .using(database)
                            .filter(processed=False)
                            .update(processed=True)
                        )
                        if recs:
                            empty = False
                    if empty:
                        if idle_loop_done:
                            break
                        else:
                            idle_loop_done = True
                            if "test" not in sys.argv:
                                # When no more messages can be found and we are not running
                                # the test suite, we try again 5 seconds later before shutting
                                # down the worker.
                                time.sleep(5)
        finally:
            for db in settings.DATABASES:
                connections[db].close()

    @classmethod
    def join(cls):
        Scenario.syncWithSettings()
        for sc in Scenario.objects.using(DEFAULT_DB_ALIAS).filter(status="In use"):
            if Comment.objects.all().using(sc.name).filter(processed=False).count():
                worker = cls._workers.get(sc.name, None)
                if worker:
                    worker.join()
                else:
                    logger.warning(
                        "Unprocessed comments but no notification factory is running"
                    )

    @classmethod
    def getFollower(cls, object_pk, content_type, user, database=DEFAULT_DB_ALIAS):
        """
        Return True the follower object when the user is following this object.
        Return False when the user isn't following this object.
        """
        model = content_type.model_class()
        if "view" in model._meta.default_permissions:
            view_permission = "%s.view_%s" % (
                model._meta.app_label,
                model._meta.model_name,
            )
            if not user.has_perm(view_permission):
                # The user isn't allowed to see this object or it's notifications
                return False
        dummy = Comment(type="comment", content_type=content_type, object_pk=object_pk)
        cls._buildRegistry()
        meta = cls._reg.get(content_type.model_class(), None)
        if meta:
            for flw in (
                Follower.objects.all().using(database).filter(user=user).order_by("id")
            ):
                for c in meta:
                    if flw.content_type.model_class() in c.messages and (
                        (
                            flw.content_type == dummy.content_type
                            and flw.object_pk == "all"
                        )
                        or c(flw, dummy)
                    ):
                        return True
        return False

    @classmethod
    def getAllFollowers(cls, object_pk, content_type, user, database=DEFAULT_DB_ALIAS):
        """
        Returns a json object with:
        - list of possible related objects to follow
        - list of notifications we already get
        - list of active users and whether they follow this object
        """
        # Loop over all followers (current user and others)
        # - build a list of all users following this object (directly or indirectly)
        # - collect info on how we follow this object and keep highest one
        followers = {}
        parents = []
        children = {}
        model = content_type.model_class()
        view_permission = (
            "%s.view_%s" % (model._meta.app_label, model._meta.model_name)
            if "view" in model._meta.default_permissions
            else None
        )
        dummy = Comment(type="comment", content_type=content_type, object_pk=object_pk)
        modelname = "%s.%s" % (model._meta.app_label, model._meta.model_name)
        status = {
            "users": [],
            "object_pk": object_pk,
            "label": force_text(model._meta.verbose_name),
            "model": modelname,
            "type": "online",
            "models": [
                {
                    "model": modelname,
                    "label": force_text(model._meta.verbose_name),
                    "checked": False,
                }
            ],
        }
        cls._buildRegistry()
        meta = cls._reg.get(model, None)
        if meta:
            for c in meta:
                if c.follower == model:
                    for m in c.messages:
                        key = "%s.%s" % (m._meta.app_label, m._meta.model_name)
                        if key not in children and m != model:
                            children[key] = {
                                "model": key,
                                "label": force_text(m._meta.verbose_name_plural),
                                "checked": False,
                            }
            for flw in (
                Follower.objects.all()
                .using(database)
                .filter(user__is_active=True)
                .order_by("id")
            ):
                for c in meta:
                    try:
                        if (
                            (flw.user not in followers or flw.user == user)
                            and flw.content_type.model_class() in c.messages
                            and (flw.object_pk == "all" or c(flw, dummy))
                            and (
                                not view_permission
                                or flw.user.has_perm(view_permission)
                            )
                        ):
                            if flw.user == user:
                                if (
                                    flw.content_type == content_type
                                    and flw.object_pk == object_pk
                                ):
                                    # You are directly following this object.
                                    args = (
                                        flw.args.get("sub", None) if flw.args else None
                                    )
                                    if args:
                                        for m in args:
                                            if m in children:
                                                children[m]["checked"] = True
                                            elif m == modelname:
                                                status["models"][0]["checked"] = True
                                    else:
                                        for ch in children.values():
                                            ch["checked"] = True
                                        status["models"][0]["checked"] = True
                                    status["type"] = (
                                        "email" if flw.type == "M" else "online"
                                    )
                                else:
                                    # You are following a parent object
                                    parents.append(
                                        {
                                            "url": flw.getURL(database),
                                            "object_pk": flw.object_pk,
                                            "model": force_text(
                                                flw.content_type.model_class()._meta.verbose_name
                                            ),
                                        }
                                    )
                            else:
                                # Maintain a list of all users following this object
                                if (
                                    flw.content_type == content_type
                                    and flw.object_pk == object_pk
                                ):
                                    followers[flw.user.username] = (
                                        "email" if flw.type == "M" else "online"
                                    )
                                elif flw.user.username not in followers:
                                    followers[flw.user.username] = "indirect"
                    except Exception as e:
                        logger.error(
                            "Exception in notification function %s: %s" % (c, e)
                        )

        for usr in (
            User.objects.all()
            .using(database)
            .filter(is_active=True)
            .exclude(username=user.username)
            .order_by("username")
            .only("username", "avatar", "first_name", "last_name")
        ):
            status["users"].append(
                {
                    "username": usr.username,
                    "avatar": usr.avatar.filename if usr.avatar else None,
                    "first_name": usr.first_name,
                    "last_name": usr.last_name,
                    "following": followers.get(usr.username, "no"),
                }
            )
        if not status["users"]:
            del status["users"]
        else:
            status["users"].sort(key=lambda x: (x["following"], x["username"]))

        if parents:
            status["parents"] = parents
            del status["models"]
        elif children:
            status["models"] += sorted(
                [c for c in children.values()],
                key=lambda x: (not x["checked"], x["label"]),
            )
        return status


class Bucket(AuditModel):
    # Create some dummy string for common bucket names to force them to be translated.
    extra_strings = (_("day"), _("week"), _("month"), _("quarter"), _("year"))

    # Database fields
    name = models.CharField(_("name"), max_length=300, primary_key=True)
    description = models.CharField(
        _("description"), max_length=500, null=True, blank=True
    )
    level = models.IntegerField(
        _("level"), help_text=_("Higher values indicate more granular time buckets")
    )

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = _("bucket")
        verbose_name_plural = _("buckets")
        db_table = "common_bucket"


class BucketDetail(AuditModel):
    # Database fields
    id = models.AutoField(_("identifier"), primary_key=True)
    bucket = models.ForeignKey(
        Bucket, verbose_name=_("bucket"), db_index=True, on_delete=models.CASCADE
    )
    name = models.CharField(_("name"), max_length=300, db_index=True)
    startdate = models.DateTimeField(_("start date"))
    enddate = models.DateTimeField(_("end date"))

    class Manager(MultiDBManager):
        def get_by_natural_key(self, bucket, startdate):
            return self.get(bucket=bucket, startdate=startdate)

    def natural_key(self):
        return (self.bucket, self.startdate)

    objects = Manager()

    def __str__(self):
        return "%s %s" % (self.bucket.name or "", self.startdate)

    class Meta:
        verbose_name = _("bucket date")
        verbose_name_plural = _("bucket dates")
        db_table = "common_bucketdetail"
        unique_together = (("bucket", "startdate"),)
        ordering = ["bucket", "startdate"]
