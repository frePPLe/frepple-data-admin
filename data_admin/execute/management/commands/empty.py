import os
from datetime import datetime

from django.apps import apps
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.core.management.color import no_style
from django.db import connections, transaction, DEFAULT_DB_ALIAS
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext_lazy as _
from django.template.loader import render_to_string

from ...models import Task
from ....common.middleware import _thread_locals
from ....common.models import User
from ....common.report import EXCLUDE_FROM_BULK_OPERATIONS
from .... import __version__


class Command(BaseCommand):

    help = """
    This command empties the contents of all data tables in the frePPLe database.

    The following data tables are not emptied:
    - users
    - user preferences
    - permissions
    - execute log
    """

    requires_system_checks = False

    def get_version(self):
        return __version__

    def add_arguments(self, parser):
        parser.add_argument("--user", help="User running the command")
        parser.add_argument(
            "--database",
            action="store",
            dest="database",
            default=DEFAULT_DB_ALIAS,
            help="Nominates a specific database to delete data from",
        ),
        parser.add_argument(
            "--task",
            type=int,
            help="Task identifier (generated automatically if not provided)",
        ),
        parser.add_argument("--models", help="Comma-separated list of models to erase")

    def handle(self, **options):
        # Pick up options
        database = options["database"]
        if database not in settings.DATABASES:
            raise CommandError("No database settings known for '%s'" % database)
        if options["user"]:
            try:
                user = User.objects.all().using(database).get(username=options["user"])
            except Exception:
                raise CommandError("User '%s' not found" % options["user"])
        else:
            user = None
        if options["models"]:
            models = options["models"].split(",")
        else:
            models = None

        now = datetime.now()
        task = None
        try:
            # Initialize the task
            setattr(_thread_locals, "database", database)
            if options["task"]:
                try:
                    task = Task.objects.all().using(database).get(pk=options["task"])
                except Exception:
                    raise CommandError("Task identifier not found")
                if (
                    task.started
                    or task.finished
                    or task.status != "Waiting"
                    or task.name not in ("frepple_flush", "empty")
                ):
                    raise CommandError("Invalid task identifier")
                task.status = "0%"
                task.started = now
            else:
                task = Task(
                    name="empty", submitted=now, started=now, status="0%", user=user
                )
                task.arguments = "%s%s" % (
                    "--user=%s " % options["user"] if options["user"] else "",
                    "--models=%s " % options["models"] if options["models"] else "",
                )
            task.processid = os.getpid()
            task.save(using=database)

            # Create a database connection
            cursor = connections[database].cursor()

            # Get a list of all django tables in the database
            tables = set(
                connections[database].introspection.django_table_names(
                    only_existing=True
                )
            )
            ContentTypekeys = set()

            # Validate the user list of tables
            if models:
                models2tables = set()
                admin_log_positive = True
                for m in models:
                    try:
                        x = m.split(".", 1)
                        x = apps.get_model(x[0], x[1])
                        if x in EXCLUDE_FROM_BULK_OPERATIONS:
                            continue

                        ContentTypekeys.add(ContentType.objects.get_for_model(x).pk)

                        x = x._meta.db_table
                        if x not in tables:
                            raise
                        models2tables.add(x)
                    except Exception as e:
                        raise CommandError("Invalid model to erase: %s" % m)
                tables = models2tables
            else:
                admin_log_positive = False
                for i in EXCLUDE_FROM_BULK_OPERATIONS:
                    tables.discard(i._meta.db_table)
                    ContentTypekeys.add(ContentType.objects.get_for_model(i).pk)
            tables.discard("auth_group_permissions")
            tables.discard("auth_permission")
            tables.discard("auth_group")
            tables.discard("django_session")
            tables.discard("common_user")
            tables.discard("common_user_groups")
            tables.discard("common_user_user_permissions")
            tables.discard("common_preference")
            tables.discard("django_content_type")
            tables.discard("execute_log")
            tables.discard("execute_schedule")
            tables.discard("common_scenario")

            # Delete all records from the tables.
            with transaction.atomic(using=database, savepoint=False):
                if ContentTypekeys:
                    if admin_log_positive:
                        cursor.execute(
                            "delete from common_comment where content_type_id = any(%s) and type in ('add', 'change', 'delete')",
                            (list(ContentTypekeys),),
                        )
                    else:
                        cursor.execute(
                            "delete from common_comment where content_type_id != any(%s) and type in ('add', 'change', 'delete')",
                            (list(ContentTypekeys),),
                        )
                if "common_bucket" in tables:
                    cursor.execute("update common_user set horizonbuckets = null")
                for stmt in connections[database].ops.sql_flush(no_style(), tables, []):
                    cursor.execute(stmt)

            # Task update
            task.status = "Done"
            task.finished = datetime.now()
            task.processid = None
            task.save(using=database)

        except Exception as e:
            if task:
                task.status = "Failed"
                task.message = "%s" % e
                task.finished = datetime.now()
                task.processid = None
                task.save(using=database)
            raise CommandError("%s" % e)

        finally:
            setattr(_thread_locals, "database", None)

    title = _("Empty the database")
    index = 1700
    help_url = "command-reference.html#empty"

    @staticmethod
    def getHTML(request):
        if request.user.has_perm("auth.run_db"):
            return render_to_string(
                "commands/empty.html",
                request=request,
            )
        else:
            return None
