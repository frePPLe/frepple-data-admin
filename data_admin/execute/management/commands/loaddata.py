#
# Copyright (C) 2018 by frePPLe bv
#
# This library is free software; you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero
# General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

from datetime import datetime
import os

from django.apps import apps
from django.conf import settings
from django.core.management.base import CommandError
from django.core.management.commands import loaddata
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _

from ....common.models import User
from ....common.middleware import _thread_locals
from ...models import Task


class Command(loaddata.Command):
    @staticmethod
    def getHTML(request):
        # Loop over all fixtures of all apps and directories
        fixtures = set()
        folders = list(settings.FIXTURE_DIRS)
        for app in apps.get_app_configs():
            if not app.name.startswith("django"):
                folders.append(
                    os.path.join(os.path.dirname(app.path), app.label, "fixtures")
                )
        for f in folders:
            try:
                for root, dirs, files in os.walk(f):
                    for i in files:
                        if i.endswith(".json"):
                            fixtures.add(i.split(".")[0])
            except Exception:
                pass  # Silently ignore failures
        fixtures = sorted(fixtures)

        return render_to_string(
            "commands/loaddata.html", {"fixtures": fixtures}, request=request
        )

    title = _("Load a dataset")
    index = 1800
    help_url = "command-reference.html#loaddata"

    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument(
            "--task",
            dest="task",
            type=int,
            help="Task identifier (generated automatically if not provided)",
        )
        parser.add_argument("--user", dest="user", help="User running the command")

    def handle(self, *fixture_labels, **options):

        # get the database object
        database = options["database"]
        if database not in settings.DATABASES:
            raise CommandError("No database settings known for '%s'" % database)

        now = datetime.now()
        task = None
        try:
            setattr(_thread_locals, "database", database)
            # Initialize the task
            if options["task"]:
                try:
                    task = Task.objects.all().using(database).get(pk=options["task"])
                except Exception:
                    raise CommandError("Task identifier not found")
                if (
                    task.started
                    or task.finished
                    or task.status != "Waiting"
                    or task.name != "loaddata"
                ):
                    raise CommandError("Invalid task identifier")
                task.status = "0%"
                task.started = now
                task.processid = os.getpid()
                task.save(
                    using=database, update_fields=["started", "status", "processid"]
                )
            else:
                if options["user"]:
                    try:
                        user = (
                            User.objects.all()
                            .using(database)
                            .get(username=options["user"])
                        )
                    except Exception:
                        raise CommandError("User '%s' not found" % options["user"])
                else:
                    user = None
                task = Task(
                    name="loaddata",
                    submitted=now,
                    started=now,
                    status="0%",
                    user=user,
                    arguments=" ".join(fixture_labels),
                )
                task.processid = os.getpid()
                task.save(using=database)

            # Excecute the standard django command
            super().handle(*fixture_labels, **options)

            # Task update
            task.status = "Done"
            task.finished = datetime.now()
            task.processid = None
            task.save(using=database, update_fields=["status", "finished"])

        except Exception as e:
            if task:
                task.status = "Failed"
                task.message = "%s" % e
                task.finished = datetime.now()
                task.processid = None
                task.save(
                    using=database, update_fields=["status", "finished", "message"]
                )
            raise CommandError("%s" % e)

        finally:
            setattr(_thread_locals, "database", None)
