from django.core.signals import request_finished
from django.db import DEFAULT_DB_ALIAS
from django.db.models import signals
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from .. import models as common_models
from ..middleware import resetRequest


def removeModelPermissions(app, model, db=DEFAULT_DB_ALIAS, exclude=None):
    q = (
        Permission.objects.all()
        .using(db)
        .filter(content_type__app_label=app, content_type__model=model)
    )
    if exclude:
        q = q.exclude(codename__in=exclude)
    q.delete()


def createExtraPermissions(sender, using=DEFAULT_DB_ALIAS, **kwargs):
    if using != DEFAULT_DB_ALIAS:
        return
    from ..menu import menu
    from ..dashboard import Dashboard

    # Create the report permissions for the single menu instance we know about.
    menu.createReportPermissions(sender.name)

    # Create widget permissions
    Dashboard.createWidgetPermissions(sender.name)


def removePermissions(sender, using=DEFAULT_DB_ALIAS, **kwargs):
    removeModelPermissions("admin", "logentry", using)
    removeModelPermissions("contenttypes", "contenttype", using)
    Permission.objects.all().using(using).filter(codename="add_permission").delete()
    Permission.objects.all().using(using).filter(codename="change_permission").delete()
    Permission.objects.all().using(using).filter(codename="delete_permission").delete()
    Permission.objects.all().using(using).filter(codename="view_permission").delete()


signals.post_migrate.connect(removePermissions)
signals.post_migrate.connect(createExtraPermissions)
request_finished.connect(resetRequest)
