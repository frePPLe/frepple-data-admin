r"""
Main data-admin configuration file.

It is recommended not to edit this file!
Instead put all your settings in the file FREPPLE_CONFDIR/djangosettings.py.

"""
import os
import sys
import importlib
import data_admin

from django.contrib import messages
from django.utils.translation import gettext_lazy as _


# FREPPLE_APP directory
if "FREPPLE_APP" in os.environ:
    FREPPLE_APP = os.environ["FREPPLE_APP"]
else:
    FREPPLE_APP = os.path.abspath(
        os.path.join(os.path.dirname(data_admin.__file__), "..")
    )

# FREPPLE_LOGDIR directory
if "FREPPLE_LOGDIR" in os.environ:
    FREPPLE_LOGDIR = os.environ["FREPPLE_LOGDIR"]
elif os.sep == "/" and os.access("/var/log/frepple", os.W_OK):
    # Linux installation layout
    FREPPLE_LOGDIR = "/var/log/frepple"
else:
    FREPPLE_LOGDIR = os.path.abspath(os.path.join(FREPPLE_APP, "logs"))

# FREPPLE_CONFIGDIR directory
if "FREPPLE_CONFIGDIR" in os.environ:
    FREPPLE_CONFIGDIR = os.environ["FREPPLE_CONFIGDIR"]
elif os.sep == "/" and os.path.isfile("/etc/frepple/djangosettings.py"):
    # Linux installation layout
    FREPPLE_CONFIGDIR = "/etc/frepple"
else:
    FREPPLE_CONFIGDIR = FREPPLE_APP

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

LANGUAGE_CODE = "en"

# Google analytics code to report usage statistics to.
# The value None disables this feature.
GOOGLE_ANALYTICS = None

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


# A list of strings representing the host/domain names the application can serve.
# This is a security measure to prevent an attacker from poisoning caches and
# password reset emails with links to malicious hosts by submitting requests
# with a fake HTTP Host header, which is possible even under many seemingly-safe
# webserver configurations.
# Values in this list can be fully qualified names (e.g. 'www.example.com'),
# in which case they will be matched against the request's Host header exactly
# (case-insensitive, not including port).
# A value beginning with a period can be used as a subdomain wildcard: '.example.com'
# will match example.com, www.example.com, and any other subdomain of example.com.
# A value of '*' will match anything, effectively disabling this feature.
# This option is only active when DEBUG = false.
ALLOWED_HOSTS = ["*"]

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = "Europe/Brussels"

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

# The default redirects URLs not ending with a slash.
# This causes trouble in combination with the DatabaseSelectionMiddleware.
# We prefer not to redirect and report this as an incorrect URL.
APPEND_SLASH = False

WSGI_APPLICATION = "data_admin.wsgi.application"
ROOT_URLCONF = "data_admin.urls"
if "FREPPLE_STATIC" in os.environ:
    STATIC_ROOT = os.environ["FREPPLE_STATIC"]
elif os.sep == "/" and os.path.isdir("/usr/share/frepple/static"):
    # Standard Linux installation
    STATIC_ROOT = "/usr/share/frepple/static"
else:
    # All other layout types
    STATIC_ROOT = os.path.normpath(os.path.join(FREPPLE_APP, "static"))
STATIC_URL = "/static/"
USE_L10N = True  # Represent data in the local format
USE_I18N = True  # Use translated strings

# A boolean that specifies if datetimes will be timezone-aware by default or not.
# If this is set to True, we will use timezone-aware datetimes internally.
# Otherwise, we use naive datetimes in local time.
USE_TZ = False  # TODO Test with this parameter set to True

# Sessions
SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"
SESSION_COOKIE_NAME = "sessionid"  # Cookie name. This can be whatever you want.
SESSION_COOKIE_AGE = 60 * 60 * 24 * 2  # Age of cookie, in seconds: 2 days
SESSION_COOKIE_DOMAIN = None  # A string, or None for standard domain cookie.
SESSION_SAVE_EVERY_REQUEST = True  # Whether to save the session data on every request.
# Needs to be True to have the breadcrumbs working correctly!
SESSION_EXPIRE_AT_BROWSER_CLOSE = (
    True  # Whether sessions expire when a user closes his browser.
)

MESSAGE_STORAGE = "django.contrib.messages.storage.fallback.SessionStorage"

TEST_RUNNER = "django.test.runner.DiscoverRunner"

DATABASE_ROUTERS = ["data_admin.common.models.MultiDBRouter"]

CSRF_FAILURE_VIEW = "data_admin.common.views.csrf_failure"

# Settings for user uploaded files
MEDIA_URL = "/uploads/"  # Do not change this
# This list of allowed extensions is what github.com allows.
# Be VERY careful about security when enlarging this list!
MEDIA_EXTENSIONS = ".gif,.jpeg,.jpg,.png,.docx,.gz,.log,.pdf,.pptx,.txt,.xlsx,.zip"
# Number of seconds a browser can cache uploaded content
MEDIA_MAX_AGE = 12 * 3600

# Backends for user authentication and authorization.
# FrePPLe currently supports only this custom one.
AUTHENTICATION_BACKENDS = ("data_admin.common.auth.MultiDBBackend",)

# Custom user model
AUTH_USER_MODEL = "common.User"

# IP address of the machine you are browsing from. When logging in from this
# machine additional debugging statements can be shown.
INTERNAL_IPS = ("127.0.0.1",)

# Default charset to use for all ``HttpResponse`` objects, if a MIME type isn't
# manually specified.
DEFAULT_CHARSET = "utf-8"

BRANDING = "frePPLe data admin"

# Default characterset for writing and reading CSV files.
# We are assuming here that the default encoding of clients is the same as the server.
# If the server is on Linux and the clients are using Windows, this guess will not be good.
# For Windows clients you should set this to the encoding that is better suited for Excel or
# other office tools.
#    Windows - western europe -> 'cp1252'
CSV_CHARSET = "utf-8"  # locale.getdefaultlocale()[1]

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

# A list of user names thatcan generate database dumps and download them.
# Since a database dump exposes all data, enabling this functionality should only be done
# for system administrators that know what they are doing.
SUPPORT_USERS = []

# Website where all documentation is available.
# - The DOCUMENTATION_URL is used as the main URL for the about box
# - The documentation is expected to be found in 'DOCUMENTATION_URL/docs/MAJOR_VERSION.MINOR_VERSION"
# - The URL shouldn't have an ending slash
DOCUMENTATION_URL = "https://frepple.org"

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
            {"width": 6, "widgets": [("welcome", {})]},
            {"width": 6, "widgets": [("news", {})]},
        ],
    },
    {
        "rowname": _("activity"),
        "cols": [
            {"width": 6, "widgets": [("recent_comments", {"limit": 10})]},
            {"width": 6, "widgets": [("recent_actions", {"limit": 10})]},
        ],
    },
]

GLOBAL_PREFERENCES = {}

# Max total log files size in MB, if the limit is reached deletes the oldest.
MAXTOTALLOGFILESIZE = 200

# Google analytics code to report usage statistics to.
# The default value of None disables this feature.
GOOGLE_ANALYTICS = None

# Adress and port number for the runwebserver command, the Windows system tray
# executable and the Windows service
ADDRESS = "0.0.0.0"
PORT = 8000

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.DjangoModelPermissions"],
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.BasicAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ),
    "DEFAULT_RENDERER_CLASSES": (
        "rest_framework.renderers.JSONRenderer",
        "data_admin.common.api.renderers.freppleBrowsableAPI",
    ),
}

# Bootstrap
DAB_FIELD_RENDERER = "django_admin_bootstrapped.renderers.BootstrapFieldRenderer"
MESSAGE_TAGS = {
    messages.SUCCESS: "alert-success",
    messages.WARNING: "alert-warning",
    messages.ERROR: "alert-danger",
    messages.INFO: "alert-success",
    messages.DEBUG: "alert-danger",
}

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "builtins": ["data_admin.common.templatetags"],
            "context_processors": [
                "data_admin.common.contextprocessors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.i18n",
                "django.template.context_processors.static",
            ],
        },
    }
]

LOCALE_PATHS = (os.path.normpath(os.path.join(FREPPLE_APP, "data_admin", "locale")),)

SILENCED_SYSTEM_CHECKS = ["admin.E408"]

# Override any of the above settings from a separate file
# for x in ("djangosettings.py", "localsettings.py"):
#     if os.access(os.path.join(FREPPLE_CONFIGDIR, x), os.R_OK):
#         with open(os.path.join(FREPPLE_CONFIGDIR, x)) as mysettingfile:
#             exec(mysettingfile.read(), globals())

# Some Django settings we don't like to be overriden
MANAGERS = ADMINS
MEDIA_ROOT = os.path.join(FREPPLE_LOGDIR, "uploads")
