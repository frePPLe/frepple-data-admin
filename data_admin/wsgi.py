"""
Configuration for data-admin WSGI web application.
This is used by the different WSGI deployment options:
  - mod_wsgi on apache web server, Gunicorn or uWSGI.
    See https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
  - django development server 'frepplectl.py runserver'
"""

import os
import sys

# Assure frePPLe is found in the Python path.
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

os.environ["LC_ALL"] = "en_US.UTF-8"
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "data_admin.settings")

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
