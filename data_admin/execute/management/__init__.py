from django.db import DEFAULT_DB_ALIAS
from django.db.models import signals
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType


def updatePermissions(using=DEFAULT_DB_ALIAS, **kwargs):
    p = Permission.objects.get_or_create(
        codename="run_db",
        content_type=ContentType.objects.get(model="permission", app_label="auth"),
    )[0]
    p.name = "Run database operations"
    p.save()


signals.post_migrate.connect(updatePermissions)
