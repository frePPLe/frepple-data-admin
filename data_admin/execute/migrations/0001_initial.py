import data_admin.common.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Task",
            fields=[
                (
                    "id",
                    models.AutoField(
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        verbose_name="identifier",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        db_index=True,
                        editable=False,
                        max_length=50,
                        verbose_name="name",
                    ),
                ),
                (
                    "submitted",
                    models.DateTimeField(editable=False, verbose_name="submitted"),
                ),
                (
                    "started",
                    models.DateTimeField(
                        blank=True, editable=False, null=True, verbose_name="started"
                    ),
                ),
                (
                    "finished",
                    models.DateTimeField(
                        blank=True, editable=False, null=True, verbose_name="submitted"
                    ),
                ),
                (
                    "arguments",
                    models.TextField(
                        editable=False,
                        max_length=200,
                        null=True,
                        verbose_name="arguments",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        editable=False, max_length=20, verbose_name="status"
                    ),
                ),
                (
                    "message",
                    models.TextField(
                        editable=False,
                        max_length=200,
                        null=True,
                        verbose_name="message",
                    ),
                ),
                (
                    "logfile",
                    models.TextField(
                        editable=False,
                        max_length=200,
                        null=True,
                        verbose_name="log file",
                    ),
                ),
                (
                    "processid",
                    models.IntegerField(
                        editable=False, null=True, verbose_name="processid"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        editable=False,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="tasks",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="user",
                    ),
                ),
            ],
            options={
                "verbose_name": "task",
                "verbose_name_plural": "tasks",
                "db_table": "execute_log",
                "default_permissions": ["view"],
            },
        ),
        migrations.CreateModel(
            name="ScheduledTask",
            fields=[
                (
                    "name",
                    models.CharField(
                        db_index=True,
                        max_length=300,
                        primary_key=True,
                        serialize=False,
                        verbose_name="name",
                    ),
                ),
                (
                    "next_run",
                    models.DateTimeField(
                        blank=True, db_index=True, null=True, verbose_name="nextrun"
                    ),
                ),
                (
                    "email_failure",
                    models.CharField(
                        blank=True,
                        max_length=300,
                        null=True,
                        verbose_name="email_failure",
                    ),
                ),
                (
                    "email_success",
                    models.CharField(
                        blank=True,
                        max_length=300,
                        null=True,
                        verbose_name="email_success",
                    ),
                ),
                ("data", data_admin.common.fields.JSONBField(blank=True, null=True)),
                (
                    "user",
                    models.ForeignKey(
                        editable=False,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="schedules",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "scheduled task",
                "verbose_name_plural": "scheduled tasks",
                "db_table": "execute_schedule",
            },
        ),
    ]
