#!/usr/bin/env python3

# This is nothing but a renamed version of django's "manage.py" command.
# We renamed it because "manage" is too generic.

import os
import sys

if __name__ == "__main__":
    # Initialize Python virtual environments
    if "VIRTUAL_ENV" in os.environ:
        activate_script = os.path.join(
            os.environ["VIRTUAL_ENV"],
            "Scripts" if os.name == "nt" else "bin",
            "activate_this.py",
        )
        exec(open(activate_script).read(), {"__file__": activate_script})

    # Initialize django
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "data_admin.settings")
    try:
        import django
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable?"
        ) from exc
    django.setup()

    # Synchronize the scenario table with the settings
    from data_admin.common.models import Scenario

    Scenario.syncWithSettings()

    # Run the command
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
