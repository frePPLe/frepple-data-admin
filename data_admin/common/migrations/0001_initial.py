from datetime import datetime

import data_admin.common.fields
from django.conf import settings
import django.contrib.auth.models
from django.contrib.auth.hashers import make_password
import django.contrib.auth.validators
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


def createAdminUser(apps, schema_editor):
    if not schema_editor.connection.alias == "default":
        return
    User = apps.get_model("common", "User")
    usr = User(
        username="admin",
        email="your@company.com",
        first_name="admin",
        last_name="admin",
        date_joined=datetime(2000, 1, 1),
        horizontype=True,
        horizonlength=6,
        horizonunit="month",
        language="auto",
        is_superuser=True,
        is_staff=True,
        is_active=True,
    )
    usr._password = "admin"
    usr.password = make_password("admin")
    usr.save()


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
        ("auth", "0011_update_proxy_permissions"),
    ]

    operations = [
        migrations.CreateModel(
            name="SystemMessage",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
            ],
            options={
                "managed": False,
                "default_permissions": (),
            },
        ),
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "username",
                    models.CharField(
                        error_messages={
                            "unique": "A user with that username already exists."
                        },
                        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
                        max_length=150,
                        unique=True,
                        validators=[
                            django.contrib.auth.validators.UnicodeUsernameValidator()
                        ],
                        verbose_name="username",
                    ),
                ),
                (
                    "first_name",
                    models.CharField(
                        blank=True, max_length=30, verbose_name="first name"
                    ),
                ),
                (
                    "last_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="last name"
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        blank=True, max_length=254, verbose_name="email address"
                    ),
                ),
                (
                    "is_staff",
                    models.BooleanField(
                        default=False,
                        help_text="Designates whether the user can log into this admin site.",
                        verbose_name="staff status",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",
                        verbose_name="active",
                    ),
                ),
                (
                    "date_joined",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="date joined"
                    ),
                ),
                (
                    "language",
                    models.CharField(
                        choices=[
                            ("auto", "Detect automatically"),
                            ("en", "English"),
                            ("fr", "French"),
                            ("de", "German"),
                            ("he", "Hebrew"),
                            ("hr", "Croatian"),
                            ("it", "Italian"),
                            ("ja", "Japanese"),
                            ("nl", "Dutch"),
                            ("pt", "Portuguese"),
                            ("pt-br", "Brazilian Portuguese"),
                            ("ru", "Russian"),
                            ("es", "Spanish"),
                            ("zh-hans", "Simplified Chinese"),
                            ("zh-hant", "Traditional Chinese"),
                            ("uk", "Ukrainian"),
                        ],
                        default="auto",
                        max_length=10,
                        verbose_name="language",
                    ),
                ),
                (
                    "theme",
                    models.CharField(
                        choices=[
                            ("earth", "Earth"),
                            ("grass", "Grass"),
                            ("lemon", "Lemon"),
                            ("odoo", "Odoo"),
                            ("openbravo", "Openbravo"),
                            ("orange", "Orange"),
                            ("snow", "Snow"),
                            ("strawberry", "Strawberry"),
                            ("water", "Water"),
                        ],
                        default="earth",
                        max_length=20,
                        verbose_name="theme",
                    ),
                ),
                (
                    "pagesize",
                    models.PositiveIntegerField(default=100, verbose_name="page size"),
                ),
                (
                    "horizonbuckets",
                    models.CharField(blank=True, max_length=300, null=True),
                ),
                ("horizonstart", models.DateTimeField(blank=True, null=True)),
                ("horizonend", models.DateTimeField(blank=True, null=True)),
                ("horizontype", models.BooleanField(blank=True, default=True)),
                (
                    "horizonlength",
                    models.IntegerField(blank=True, default=6, null=True),
                ),
                (
                    "horizonbefore",
                    models.IntegerField(blank=True, default=0, null=True),
                ),
                (
                    "horizonunit",
                    models.CharField(
                        blank=True,
                        choices=[("day", "day"), ("week", "week"), ("month", "month")],
                        default="month",
                        max_length=5,
                        null=True,
                    ),
                ),
                ("avatar", models.ImageField(blank=True, null=True, upload_to="")),
                (
                    "lastmodified",
                    models.DateTimeField(
                        auto_now=True,
                        db_index=True,
                        null=True,
                        verbose_name="last modified",
                    ),
                ),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.Group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.Permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "verbose_name": "user",
                "verbose_name_plural": "users",
                "db_table": "common_user",
            },
            managers=[
                ("objects", django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name="Bucket",
            fields=[
                (
                    "source",
                    models.CharField(
                        blank=True,
                        db_index=True,
                        max_length=300,
                        null=True,
                        verbose_name="source",
                    ),
                ),
                (
                    "lastmodified",
                    models.DateTimeField(
                        db_index=True,
                        default=django.utils.timezone.now,
                        editable=False,
                        verbose_name="last modified",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        max_length=300,
                        primary_key=True,
                        serialize=False,
                        verbose_name="name",
                    ),
                ),
                (
                    "description",
                    models.CharField(
                        blank=True,
                        max_length=500,
                        null=True,
                        verbose_name="description",
                    ),
                ),
                (
                    "level",
                    models.IntegerField(
                        help_text="Higher values indicate more granular time buckets",
                        verbose_name="level",
                    ),
                ),
            ],
            options={
                "verbose_name": "bucket",
                "verbose_name_plural": "buckets",
                "db_table": "common_bucket",
            },
        ),
        migrations.CreateModel(
            name="Comment",
            fields=[
                (
                    "id",
                    models.AutoField(
                        primary_key=True, serialize=False, verbose_name="identifier"
                    ),
                ),
                (
                    "type",
                    models.CharField(
                        choices=[
                            ("add", "Add"),
                            ("change", "Change"),
                            ("delete", "Delete"),
                            ("comment", "comment"),
                            ("follower", "follower"),
                        ],
                        default="add",
                        max_length=10,
                        verbose_name="type",
                    ),
                ),
                (
                    "object_repr",
                    models.CharField(max_length=200, verbose_name="object repr"),
                ),
                ("object_pk", models.TextField(verbose_name="object id")),
                ("comment", models.TextField(max_length=3000, verbose_name="message")),
                (
                    "attachment",
                    models.FileField(
                        blank=True,
                        null=True,
                        upload_to="",
                        validators=[
                            django.core.validators.FileExtensionValidator(
                                allowed_extensions=[
                                    "gif",
                                    "jpeg",
                                    "jpg",
                                    "png",
                                    "docx",
                                    "gz",
                                    "log",
                                    "pdf",
                                    "pptx",
                                    "txt",
                                    "xlsx",
                                    "zip",
                                ]
                            )
                        ],
                    ),
                ),
                (
                    "lastmodified",
                    models.DateTimeField(
                        db_index=True,
                        default=django.utils.timezone.now,
                        editable=False,
                        verbose_name="last modified",
                    ),
                ),
                (
                    "processed",
                    models.BooleanField(
                        db_index=True, default=False, verbose_name="processed"
                    ),
                ),
                (
                    "content_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="content_type_set_for_comment",
                        to="contenttypes.ContentType",
                        verbose_name="content type",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        editable=False,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="user",
                    ),
                ),
            ],
            options={
                "verbose_name": "comment",
                "verbose_name_plural": "comments",
                "db_table": "common_comment",
                "ordering": ("id",),
                "default_permissions": [],
            },
        ),
        migrations.CreateModel(
            name="Follower",
            fields=[
                (
                    "id",
                    models.AutoField(
                        primary_key=True, serialize=False, verbose_name="identifier"
                    ),
                ),
                ("object_pk", models.TextField(null=True, verbose_name="object name")),
                (
                    "type",
                    models.CharField(
                        choices=[("M", "email"), ("O", "online")],
                        default="O",
                        max_length=10,
                        verbose_name="type",
                    ),
                ),
                ("args", data_admin.common.fields.JSONBField(blank=True, null=True)),
                (
                    "content_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="contenttypes.ContentType",
                        verbose_name="model name",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="user",
                    ),
                ),
            ],
            options={
                "verbose_name": "follower",
                "verbose_name_plural": "followers",
                "db_table": "common_follower",
                "default_permissions": (),
            },
        ),
        migrations.CreateModel(
            name="Parameter",
            fields=[
                (
                    "source",
                    models.CharField(
                        blank=True,
                        db_index=True,
                        max_length=300,
                        null=True,
                        verbose_name="source",
                    ),
                ),
                (
                    "lastmodified",
                    models.DateTimeField(
                        db_index=True,
                        default=django.utils.timezone.now,
                        editable=False,
                        verbose_name="last modified",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        max_length=60,
                        primary_key=True,
                        serialize=False,
                        verbose_name="name",
                    ),
                ),
                (
                    "value",
                    models.CharField(
                        blank=True, max_length=1000, null=True, verbose_name="value"
                    ),
                ),
                (
                    "description",
                    models.CharField(
                        blank=True,
                        max_length=1000,
                        null=True,
                        verbose_name="description",
                    ),
                ),
            ],
            options={
                "verbose_name": "parameter",
                "verbose_name_plural": "parameters",
                "db_table": "common_parameter",
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Scenario",
            fields=[
                (
                    "name",
                    models.CharField(
                        max_length=300,
                        primary_key=True,
                        serialize=False,
                        verbose_name="name",
                    ),
                ),
                (
                    "description",
                    models.CharField(
                        blank=True,
                        max_length=500,
                        null=True,
                        verbose_name="description",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("free", "free"),
                            ("in use", "in use"),
                            ("busy", "busy"),
                        ],
                        max_length=10,
                        verbose_name="status",
                    ),
                ),
                (
                    "lastrefresh",
                    models.DateTimeField(
                        editable=False, null=True, verbose_name="last refreshed"
                    ),
                ),
                (
                    "help_url",
                    models.URLField(editable=False, null=True, verbose_name="help"),
                ),
            ],
            options={
                "verbose_name": "scenario",
                "verbose_name_plural": "scenarios",
                "db_table": "common_scenario",
                "ordering": ["name"],
                "default_permissions": ("copy", "release", "promote"),
            },
        ),
        migrations.CreateModel(
            name="Notification",
            fields=[
                (
                    "id",
                    models.AutoField(
                        primary_key=True, serialize=False, verbose_name="identifier"
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[("U", "unread"), ("R", "read")],
                        default="U",
                        max_length=5,
                        verbose_name="status",
                    ),
                ),
                (
                    "type",
                    models.CharField(
                        choices=[("M", "email"), ("O", "online")],
                        default="O",
                        max_length=5,
                        verbose_name="type",
                    ),
                ),
                (
                    "comment",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="common.Comment",
                        verbose_name="comment",
                    ),
                ),
                (
                    "follower",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="common.Follower",
                        verbose_name="follower",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="user",
                    ),
                ),
            ],
            options={
                "verbose_name": "notification",
                "verbose_name_plural": "notifications",
                "db_table": "common_notification",
            },
        ),
        migrations.CreateModel(
            name="UserPreference",
            fields=[
                (
                    "id",
                    models.AutoField(
                        primary_key=True, serialize=False, verbose_name="identifier"
                    ),
                ),
                ("property", models.CharField(max_length=100)),
                ("value", data_admin.common.fields.JSONBField(max_length=1000)),
                (
                    "user",
                    models.ForeignKey(
                        editable=False,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="preferences",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="user",
                    ),
                ),
            ],
            options={
                "verbose_name": "preference",
                "verbose_name_plural": "preferences",
                "db_table": "common_preference",
                "default_permissions": [],
                "unique_together": {("user", "property")},
            },
        ),
        migrations.CreateModel(
            name="BucketDetail",
            fields=[
                (
                    "source",
                    models.CharField(
                        blank=True,
                        db_index=True,
                        max_length=300,
                        null=True,
                        verbose_name="source",
                    ),
                ),
                (
                    "lastmodified",
                    models.DateTimeField(
                        db_index=True,
                        default=django.utils.timezone.now,
                        editable=False,
                        verbose_name="last modified",
                    ),
                ),
                (
                    "id",
                    models.AutoField(
                        primary_key=True, serialize=False, verbose_name="identifier"
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        db_index=True, max_length=300, verbose_name="name"
                    ),
                ),
                ("startdate", models.DateTimeField(verbose_name="start date")),
                ("enddate", models.DateTimeField(verbose_name="end date")),
                (
                    "bucket",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="common.Bucket",
                        verbose_name="bucket",
                    ),
                ),
            ],
            options={
                "verbose_name": "bucket date",
                "verbose_name_plural": "bucket dates",
                "db_table": "common_bucketdetail",
                "ordering": ["bucket", "startdate"],
                "unique_together": {("bucket", "startdate")},
            },
        ),
        migrations.RunPython(code=createAdminUser),
    ]
