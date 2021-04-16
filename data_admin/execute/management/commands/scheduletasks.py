from datetime import datetime, timedelta
from importlib import import_module
import os
import re
from shutil import which
from subprocess import call
import sys

from django.conf import settings
from django.core.mail import EmailMessage
from django.core.management import get_commands
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction, DEFAULT_DB_ALIAS
from django.db.models import Min
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _

from ...models import ScheduledTask, Task
from .... import __version__
from ....common.middleware import _thread_locals
from ....common.models import User
from ....common.report import GridReport
from .runworker import launchWorker, runTask


class Command(BaseCommand):
    help = """
        Mode 1: schedule name is passed as argument
    
        Mode 2: no schedule name is passed
        Creates new tasks in the task list, based on the schedule.
        This command is normally executed automatically, scheduled with the at-command.
        Only in rare situations would you need to run this command manually.
        """
    requires_system_checks = False

    def get_version(self):
        return __version__

    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument(
            "--database",
            default=DEFAULT_DB_ALIAS,
            help="Specify the database to run in.",
        )
        parser.add_argument("--schedule", help="Name of the scheduled task to execute")
        parser.add_argument("--user", dest="user", help="User running the command")
        parser.add_argument(
            "--task",
            type=int,
            help="Task identifier (generated automatically if not provided)",
        )

    def handle(self, *args, **options):
        # Dispatcher
        if options["schedule"]:
            self.executeScheduledTask(*args, **options)
        else:
            self.createScheduledTasks(*args, **options)

    def executeScheduledTask(self, *args, **options):
        database = options["database"]
        if database not in settings.DATABASES:
            raise CommandError("No database settings known for '%s'" % database)
        try:
            schedule = ScheduledTask.objects.using(database).get(
                name=options["schedule"]
            )
        except ScheduledTask.DoesNotExist:
            raise CommandError(
                "No scheduled task found with name '%s' " % options["schedule"]
            )
        if "user" in options and options["user"]:
            try:
                user = User.objects.all().using(database).get(username=options["user"])
            except Exception:
                raise CommandError("User '%s' not found" % options["user"])
        else:
            user = None

        task = None
        now = datetime.now()
        try:
            setattr(_thread_locals, "database", database)
            # Initialize the task
            if "task" in options and options["task"]:
                try:
                    task = Task.objects.all().using(database).get(pk=options["task"])
                except Exception:
                    raise CommandError("Task identifier not found")
                if (
                    task.started
                    or task.finished
                    or task.status != "Waiting"
                    or task.name != "scheduletasks"
                ):
                    raise CommandError("Invalid task identifier")
                task.status = "0%"
                task.started = now
                task.processid = os.getpid()
            else:
                task = Task(
                    name="scheduletasks",
                    submitted=now,
                    started=now,
                    status="0%",
                    arguments="--schedule='%s'" % schedule.name,
                    user=user,
                    processid=os.getpid(),
                )
            task.save(using=database)

            # The loop that actually executes the tasks
            tasklist = schedule.data.get("tasks", [])
            stepcount = len(tasklist)
            idx = 1
            failed = []
            for step in tasklist:
                steptask = Task(
                    name=step.get("name"),
                    submitted=datetime.now(),
                    arguments=step.get("arguments", ""),
                    user=user,
                    status="Waiting",
                )
                steptask.save(using=database)
                Task.objects.all().using(database).filter(pk=task.id).update(
                    message="Running task %s as step %s of %s"
                    % (steptask.id, idx, stepcount),
                    status="%d%%" % int(idx * 100.0 / stepcount),
                )
                runTask(steptask, database)

                # Check the status
                steptask = Task.objects.all().using(database).get(pk=steptask.id)
                if steptask.status == "Failed":
                    failed.append(str(steptask.id))
                    if step.get("abort_on_failure", False):
                        task = Task.objects.all().using(database).get(pk=task.id)
                        task.message = "Failed at step %s of %s" % (idx, len(tasklist))
                        task.status = "Failed"
                        task.finished = datetime.now()
                        task.save(
                            using=database,
                            update_fields=["message", "status", "finished"],
                        )
                        raise Exception(task.message)
                idx += 1

            # Reread the task from the database and update it
            task = Task.objects.all().using(database).get(pk=task.id)
            task.processid = None
            if failed:
                task.status = "Failed"
                task.message = "Failed at tasks: %s" % ", ".join(failed)
            else:
                task.status = "Done"
                task.message = ""
            task.finished = datetime.now()
            task.save(
                using=database,
                update_fields=["message", "status", "finished", "processid"],
            )

            # Email on success
            if schedule.email_success:
                correctedRecipients = []
                for r in schedule.email_success.split(","):
                    r = r.strip()
                    if r and re.fullmatch(r"[^@]+@[^@]+\.[^@]+", r):
                        correctedRecipients.append(r.strip())
                if not settings.EMAIL_HOST:
                    task.message = (
                        "Can't send success e-mail: missing SMTP configuration"
                    )
                    task.save(
                        using=database,
                        update_fields=["message", "status", "finished", "processid"],
                    )
                elif not correctedRecipients:
                    task.message = "Can't send success e-mail: invalid recipients"
                    task.save(
                        using=database,
                        update_fields=["message", "status", "finished", "processid"],
                    )
                else:
                    try:
                        EmailMessage(
                            subject="FrePPLe successfully executed %s" % schedule.name,
                            body="Task %s completed succesfully" % task.id,
                            to=correctedRecipients,
                        ).send()
                    except Exception as e:
                        task.message = "Can't send failure e-mail: %s" % e
                        task.save(
                            using=database,
                            update_fields=[
                                "message",
                                "status",
                                "finished",
                                "processid",
                            ],
                        )

        except Exception as e:
            if task:
                task = Task.objects.all().using(database).get(pk=task.id)
                task.status = "Failed"
                task.message = "%s" % e
                task.finished = datetime.now()
                task.processid = None
                task.save(
                    using=database,
                    update_fields=["message", "status", "finished", "processid"],
                )

                # Email on failure
                if schedule.email_failure:
                    correctedRecipients = []
                    for r in schedule.email_failure.split(","):
                        r = r.strip()
                        if r and re.fullmatch(r"[^@]+@[^@]+\.[^@]+", r):
                            correctedRecipients.append(r.strip())
                    if not settings.EMAIL_HOST:
                        task.message = (
                            "Can't send failure e-mail: missing SMTP configuration"
                        )
                        task.save(
                            using=database,
                            update_fields=[
                                "message",
                                "status",
                                "finished",
                                "processid",
                            ],
                        )
                    elif not correctedRecipients:
                        task.message = "Can't send failure e-mail: invalid recipients"
                        task.save(
                            using=database,
                            update_fields=[
                                "message",
                                "status",
                                "finished",
                                "processid",
                            ],
                        )
                    else:
                        try:
                            EmailMessage(
                                subject="FrePPLe failed executing %s" % schedule.name,
                                body="Task %s failed: %s" % (task.id, e),
                                to=correctedRecipients,
                            ).send()
                        except Exception as e:
                            task.message = "Can't send failure e-mail: %s" % e
                            task.save(
                                using=database,
                                update_fields=[
                                    "message",
                                    "status",
                                    "finished",
                                    "processid",
                                ],
                            )
            raise e

        finally:
            setattr(_thread_locals, "database", None)

    def createScheduledTasks(self, *args, **options):
        """
        Task scheduler that looks at the defined schedule and generates tasks
        at the right moment.
        """
        database = options["database"]
        if database not in settings.DATABASES:
            raise CommandError("No database settings known for '%s'" % database)

        # Collect tasks
        # Note: use transaction and select_for_update to handle concurrent access
        now = datetime.now()
        created = False
        with transaction.atomic(using=database):
            for schedule in (
                ScheduledTask.objects.all()
                .using(database)
                .filter(next_run__isnull=False, next_run__lte=now)
                .order_by("next_run", "name")
                .select_for_update(skip_locked=True)
            ):
                Task(
                    name="scheduletasks",
                    submitted=now,
                    status="Waiting",
                    user=schedule.user,
                    arguments="--schedule='%s'" % schedule.name,
                ).save(using=database)
                schedule.computeNextRun(now + timedelta(seconds=1))
                schedule.save(using=database)
                created = True

        # Launch the worker process
        if created:
            launchWorker(database)

        # Reschedule to run this task again at the next date
        earliest_next = (
            ScheduledTask.objects.using(database)
            .filter(next_run__isnull=False, next_run__gt=now)
            .aggregate(Min("next_run"))
        )["next_run__min"]
        if earliest_next:
            retcode = 0
            if os.name == "nt":
                # TODO For multi-tenancy possible we would also need to set the
                # FREPPLE_CONFIGDIR environment variable. It seems that isn't
                # possible with the Windows task scheduler.
                # TODO The task scheduler has a more powerful XML interface that
                # allows to define eg wake up of computer, run when not logged on,
                # priviliges, etc
                if "python" in sys.executable:
                    # Development layout
                    cmd = "%s %s scheduletasks --database=%s" % (
                        sys.executable.replace("python.exe", "pythonw.exe"),
                        os.path.abspath(sys.argv[0]),
                        database,
                    )
                else:
                    # Windows installer
                    cmd = '"%s" scheduletasks --database=%s' % (
                        sys.executable.replace("freppleserver.exe", "frepplectl.exe"),
                        database,
                    )
                retcode = call(
                    [
                        "schtasks",
                        "/create",
                        "/tn",
                        "frePPLe scheduler on %s" % database,
                        "/sc",
                        "once",
                        "/st",
                        earliest_next.strftime("%H:%M"),
                        "/sd",
                        earliest_next.strftime("%m/%d/%Y"),
                        "/f",
                        "/tr",
                        cmd,
                    ]
                )
            else:
                my_env = os.environ.copy()
                my_env["FREPPLE_CONFIGDIR"] = settings.FREPPLE_CONFIGDIR
                try:
                    if which("frepplectl"):
                        retcode = call(
                            "echo frepplectl scheduletasks --database=%s | at %s"
                            % (database, earliest_next.strftime("%H:%M %y-%m-%d")),
                            env=my_env,
                            shell=True,
                        )
                    else:
                        retcode = call(
                            "echo %s scheduletasks --database=%s | at %s"
                            % (
                                os.path.abspath(sys.argv[0]),
                                database,
                                earliest_next.strftime("%H:%M %y-%m-%d"),
                            ),
                            env=my_env,
                            shell=True,
                        )
                except OSError as e:
                    raise CommandError("Can't schedule the task: %s" % e)
            if retcode < 0:
                raise CommandError("Non-zero exit code when scheduling the task")

    # accordion template
    title = _("Group and schedule tasks")
    index = 500

    help_url = "command-reference.html#scheduletasks"

    @staticmethod
    def getHTML(request):
        commands = []
        for commandname, appname in get_commands().items():
            if commandname != "scheduletasks":
                try:
                    cmd = getattr(
                        import_module(
                            "%s.management.commands.%s" % (appname, commandname)
                        ),
                        "Command",
                    )
                    if getattr(cmd, "index", -1) >= 0 and getattr(cmd, "getHTML", None):
                        commands.append((cmd.index, commandname))
                except Exception:
                    pass
        commands = [i[1] for i in sorted(commands)]
        schedules = [
            s.adjustForTimezone(GridReport.getTimezoneOffset(request))
            for s in ScheduledTask.objects.all()
            .using(request.database)
            .order_by("name")
        ]
        schedules.append(ScheduledTask())  # Add an empty template
        return render_to_string(
            "commands/scheduletasks.html",
            {"schedules": schedules, "commands": commands},
            request=request,
        )
