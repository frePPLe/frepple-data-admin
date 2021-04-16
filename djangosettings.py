# -*- coding: utf-8 -*-

r"""
Main data-admin configuration file.
"""
import os
import sys

from django.utils.translation import gettext_lazy as _

try:
    DEBUG = "runserver" in sys.argv
except Exception:
    DEBUG = False
DEBUG_JS = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = "%@mzit!i8b*$zc&6oev96=RANDOMSTRING"

# FrePPLe only supports the postgresql database.
# Create additional entries in this dictionary to define scenario schemas.

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        # Database name
        "NAME": "data_admin",
        # Role name when using md5 authentication.
        # Leave as an empty string when using peer or
        # ident authencation.
        "USER": "frepple",
        # Role password when using md5 authentication.
        # Leave as an empty string when using peer or
        # ident authencation.
        "PASSWORD": "frepple",
        # When using TCP sockets specify the hostname,
        # the ip4 address or the ip6 address here.
        # Leave as an empty string to use Unix domain
        # socket ("local" lines in pg_hba.conf).
        "HOST": "",
        # Specify the port number when using a TCP socket.
        "PORT": "",
        "OPTIONS": {},
        "CONN_MAX_AGE": 60,
        "TEST": {
            "NAME": "test_frepple"  # Database name used when running the test suite.
        },
        "FILEUPLOADFOLDER": os.path.normpath(
            os.path.join(FREPPLE_LOGDIR, "data", "default")
        ),
        # Role name for executing custom reports and processing sql data files.
        # Make sure this role has properly restricted permissions!
        # When left unspecified, SQL statements run with the full read-write
        # permissions of the user specified above. Which can be handy, but is not secure.
        "SQL_ROLE": "report_role",
        "SECRET_WEBTOKEN_KEY": SECRET_KEY,
    },
    "scenario1": {
        "ENGINE": "django.db.backends.postgresql",
        # Database name
        "NAME": "data_admin_1",
        # Role name when using md5 authentication.
        # Leave as an empty string when using peer or
        # ident authencation.
        "USER": "frepple",
        # Role password when using md5 authentication.
        # Leave as an empty string when using peer or
        # ident authencation.
        "PASSWORD": "frepple",
        # When using TCP sockets specify the hostname,
        # the ip4 address or the ip6 address here.
        # Leave as an empty string to use Unix domain
        # socket ("local" lines in pg_hba.conf).
        "HOST": "",
        # Specify the port number when using a TCP socket.
        "PORT": "",
        "OPTIONS": {},
        "CONN_MAX_AGE": 60,
        "TEST": {
            "NAME": "test_scenario1"  # Database name used when running the test suite.
        },
        "FILEUPLOADFOLDER": os.path.normpath(
            os.path.join(FREPPLE_LOGDIR, "data", "scenario1")
        ),
        # Role name for executing custom reports and processing sql data files.
        # Make sure this role has properly restricted permissions!
        # When left unspecified, SQL statements run with the full read-write
        # permissions of the user specified above. Which can be handy, but is not secure.
        "SQL_ROLE": "report_role",
        "SECRET_WEBTOKEN_KEY": SECRET_KEY,
    },
    "scenario2": {
        "ENGINE": "django.db.backends.postgresql",
        # Database name
        "NAME": "data_admin_2",
        # Role name when using md5 authentication.
        # Leave as an empty string when using peer or
        # ident authencation.
        "USER": "frepple",
        # Role password when using md5 authentication.
        # Leave as an empty string when using peer or
        # ident authencation.
        "PASSWORD": "frepple",
        # When using TCP sockets specify the hostname,
        # the ip4 address or the ip6 address here.
        # Leave as an empty string to use Unix domain
        # socket ("local" lines in pg_hba.conf).
        "HOST": "",
        # Specify the port number when using a TCP socket.
        "PORT": "",
        "OPTIONS": {},
        "CONN_MAX_AGE": 60,
        "TEST": {
            "NAME": "test_scenario2"  # Database name used when running the test suite.
        },
        "FILEUPLOADFOLDER": os.path.normpath(
            os.path.join(FREPPLE_LOGDIR, "data", "scenario2")
        ),
        # Role name for executing custom reports and processing sql data files.
        # Make sure this role has properly restricted permissions!
        # When left unspecified, SQL statements run with the full read-write
        # permissions of the user specified above. Which can be handy, but is not secure.
        "SQL_ROLE": "report_role",
        "SECRET_WEBTOKEN_KEY": SECRET_KEY,
    },
    "scenario3": {
        "ENGINE": "django.db.backends.postgresql",
        # Database name
        "NAME": "data_admin_3",
        # Role name when using md5 authentication.
        # Leave as an empty string when using peer or
        # ident authencation.
        "USER": "frepple",
        # Role password when using md5 authentication.
        # Leave as an empty string when using peer or
        # ident authencation.
        "PASSWORD": "frepple",
        # When using TCP sockets specify the hostname,
        # the ip4 address or the ip6 address here.
        # Leave as an empty string to use Unix domain
        # socket ("local" lines in pg_hba.conf).
        "HOST": "",
        # Specify the port number when using a TCP socket.
        "PORT": "",
        "OPTIONS": {},
        "CONN_MAX_AGE": 60,
        "TEST": {
            "NAME": "test_scenario3"  # Database name used when running the test suite.
        },
        "FILEUPLOADFOLDER": os.path.normpath(
            os.path.join(FREPPLE_LOGDIR, "data", "scenario3")
        ),
        # Role name for executing custom reports and processing sql data files.
        # Make sure this role has properly restricted permissions!
        # When left unspecified, SQL statements run with the full read-write
        # permissions of the user specified above. Which can be handy, but is not secure.
        "SQL_ROLE": "report_role",
        "SECRET_WEBTOKEN_KEY": SECRET_KEY,
    },
}

LANGUAGE_CODE = "en"

# Google analytics code to report usage statistics to.
# The value None disables this feature.
GOOGLE_ANALYTICS = None

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = "Europe/Brussels"

BRANDING = "frePPLe data admin"

# Website where all documentation is available.
# - The DOCUMENTATION_URL is used as the main URL for the about box
# - The documentation is expected to be found in 'DOCUMENTATION_URL/docs/MAJOR_VERSION.MINOR_VERSION"
# - The URL shouldn't have an ending slash
DOCUMENTATION_URL = "http://your-website-with-documentation"

# Supported language codes, sorted by language code.
# Language names and codes should match the ones in Django.
# You can see the list supported by Django at:
#    https://github.com/django/django/blob/master/django/conf/global_settings.py
LANGUAGES = (
    ("en", _("English")),
    ("fr", _("French")),
    ("de", _("German")),
    ("he", _("Hebrew")),
    ("hr", _("Croatian")),
    ("it", _("Italian")),
    ("ja", _("Japanese")),
    ("nl", _("Dutch")),
    ("pt", _("Portuguese")),
    ("pt-br", _("Brazilian Portuguese")),
    ("ru", _("Russian")),
    ("es", _("Spanish")),
    ("zh-hans", _("Simplified Chinese")),
    ("zh-hant", _("Traditional Chinese")),
    ("uk", _("Ukrainian")),
)

# The remember-me checkbox on the login page allows to keep a session cookie
# active in your browser. The session will expire after the age configured
# in the setting below (epxressed in seconds).
# Set the value to 0 to force users to log in for every browser session.
SESSION_COOKIE_AGE = 3600 * 24 * 3  # 3 days

MIDDLEWARE = (
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    # Uncomment the next line to automatically log on as the admin user,
    # which can be useful for development or for demo models.
    # 'freppledb.common.middleware.AutoLoginAsAdminUser',
    "data_admin.common.middleware.MultiDBMiddleware",
    # Optional: The following middleware allows authentication with HTTP headers
    "data_admin.common.middleware.HTTPAuthenticationMiddleware",
    "data_admin.common.middleware.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
)

# Installed applications.
# The order is important: urls, templates and menus of the earlier entries
# take precedence over and override later entries.
INSTALLED_APPS = (
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "data_admin.boot",
    # Add any project specific apps here
    "data_admin_examples.example1",
    "data_admin.execute",
    "data_admin.common",
    "django_filters",
    "rest_framework",
    "django_admin_bootstrapped",
    "django.contrib.admin",
)

# Custom attribute fields in the database
# After each change of this setting, the following commands MUST be
# executed to create the fields in the database(s).
#   frepplectl makemigrations
#   frepplectl migrate     OR     frepplectl migrate --database DATABASE
#
# The commands will create migration files to keep track of the changes.
# You MUST use the above commands and the generated migration scripts. Manually
# changing the database schema will work in simple cases, but will get you
# in trouble in the long run!
# You'll need write permissions in the folder where these are stored.
#
# See https://docs.djangoproject.com/en/1.8/topics/migrations/ for the
# details on the migration files. For complex changes to the attributes
# an administrator may need to edit, delete or extend these files.
#
# Supported field types are 'string', 'boolean', 'number', 'integer',
# 'date', 'datetime', 'duration' and 'time'.
# Example:
#  ATTRIBUTES = [
#    ('freppledb.input.models.Item', [
#      ('attribute1', ugettext('attribute_1'), 'string'),
#      ('attribute2', ugettext('attribute_2'), 'boolean'),
#      ('attribute3', ugettext('attribute_3'), 'date'),
#      ('attribute4', ugettext('attribute_4'), 'datetime'),
#      ('attribute5', ugettext('attribute_5'), 'number'),
#      ]),
#    ('freppledb.input.models.Operation', [
#      ('attribute1', ugettext('attribute_1'), 'string'),
#      ])
#    ]
ATTRIBUTES = []

LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "filters": {"require_debug_false": {"()": "django.utils.log.RequireDebugFalse"}},
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s"
        },
        "simple": {"format": "%(levelname)s %(message)s"},
    },
    "handlers": {
        "null": {"level": "DEBUG", "class": "logging.NullHandler"},
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
        "mail_admins": {
            "level": "CRITICAL",
            "filters": ["require_debug_false"],
            "class": "django.utils.log.AdminEmailHandler",
        },
    },
    "loggers": {
        # A handler to log all SQL queries.
        # The setting "DEBUG" also needs to be set to True higher up in this file.
        #'django.db.backends': {
        #    'handlers': ['console'],
        #    'level': 'DEBUG',
        #    'propagate': False,
        # },
        "django": {"handlers": ["console"], "level": "INFO"},
        "data_admin": {"handlers": ["console"], "level": "INFO"},
    },
}

# Max total log files size in MB, if the limit is reached deletes the oldest.
MAXTOTALLOGFILESIZE = 200

# A list of available user interface themes.
# If multiple themes are configured in this list, the user's can change their
# preferences among the ones listed here.
# If the list contains only a single value, the preferences screen will not
# display users an option to choose the theme.
THEMES = [
    "earth",
    "grass",
    "lemon",
    "odoo",
    "openbravo",
    "orange",
    "snow",
    "strawberry",
    "water",
]

# A default user-group to which new users are automatically added
DEFAULT_USER_GROUP = None

# The default user interface theme
DEFAULT_THEME = "earth"

# The default number of records to pull from the server as a page
DEFAULT_PAGESIZE = 100

# Configuration of the default dashboard
DEFAULT_DASHBOARD = [
    {
        "rowname": _("Welcome"),
        "cols": [
            {"width": 8, "widgets": [("inbox", {"limit": 10})]},
            {"width": 4, "widgets": [("news", {})]},
        ],
    },
]

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {"min_length": 8},
    },
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Configuration of SMTP mail server
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = "your_email@domain.com"
SERVER_EMAIL = "your_email@domain.com"
EMAIL_HOST_USER = "your_email@domain.com"
EMAIL_HOST_PASSWORD = "frePPLeIsTheBest"
EMAIL_HOST = None
EMAIL_PORT = 25
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

# Port number when not using Apache
PORT = 8000

# Settings for user uploaded files
MEDIA_URL = "/uploads/"  # Do not change this
# This list of allowed extensions is what github.com allows.
# Be VERY careful about security when enlarging this list!
MEDIA_EXTENSIONS = ".gif,.jpeg,.jpg,.png,.docx,.gz,.log,.pdf,.pptx,.txt,.xlsx,.zip"
# Number of seconds a browser can cache uploaded content
MEDIA_MAX_AGE = 12 * 3600

# Browser to test with selenium
SELENIUM_TESTS = "chrome"
SELENIUM_HEADLESS = True
