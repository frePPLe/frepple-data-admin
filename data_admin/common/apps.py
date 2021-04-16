import os

from django.apps import AppConfig
from django.conf import settings
from django.core import checks
from django.core.exceptions import ImproperlyConfigured
from django.utils.autoreload import autoreload_started


def watchDjangoSettings(sender, **kwargs):
    sender.watch_file(os.path.join(settings.FREPPLE_CONFIGDIR, "djangosettings.py"))
    sender.watch_file(os.path.join(settings.FREPPLE_CONFIGDIR, "localsettings.py"))


@checks.register()
def check_python_packages(app_configs, **kwargs):
    """
    Check whether all required python packages are available.
    """
    errors = []
    for p in [
        ("rest_framework", "djangorestframework"),
        ("rest_framework_bulk", "djangorestframework-bulk"),
        ("rest_framework_filters", "djangorestframework-filters"),
        ("django_admin_bootstrapped", "django-admin-bootstrapped"),
        ("bootstrap3", "django-bootstrap3"),
        ("django_filters", "django-filter"),
        ("html5lib", "html5lib"),
        ("jdcal", "jdcal"),
        ("markdown", "markdown"),
        ("openpyxl", "openpyxl"),
        ("lxml", "lxml"),
        ("jwt", "PyJWT"),
        ("requests", "requests"),
        ("dateutil", "python-dateutil"),
    ]:
        try:
            __import__(p[0])
        except ModuleNotFoundError:
            errors.append(
                checks.Error(
                    "Missing python package '%s'" % p[1],
                    hint="Install with 'pip3 install %s'" % p[1],
                    obj=None,
                    id="frepple.dependency",
                )
            )
    return errors


class CommonConfig(AppConfig):
    name = "data_admin.common"
    verbose_name = "common"

    def ready(self):
        autoreload_started.connect(watchDjangoSettings)

        # Validate all required modules are activated
        missing = []
        required_apps = [
            "django.contrib.auth",
            "django.contrib.contenttypes",
            "django.contrib.messages",
            "django.contrib.staticfiles",
            "data_admin.boot",
            "data_admin.execute",
            "data_admin.common",
            "django_filters",
            "rest_framework",
            "django_admin_bootstrapped",
            "django.contrib.admin",
        ]
        for app in required_apps:
            if app not in settings.INSTALLED_APPS:
                missing.append(app)
        if missing:
            raise ImproperlyConfigured(
                "Missing required apps in INSTALLED_APPS: %s" % ", ".join(missing)
            )
