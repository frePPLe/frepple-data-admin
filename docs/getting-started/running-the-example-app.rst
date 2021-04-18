=======================
Running the example app
=======================

In this section, we'll run the example application that comes with the installation.

* :ref:`example_config`
* :ref:`example_initialize`
* :ref:`example_runserver`


.. _example_config:

Edit the djangosettings.py configuration file
---------------------------------------------

The python package provides a configuration file "djangosettings.py".
Open this file with a text editor and review the following sections:

* DATABASES:

  The minimal content for this block is as follows. The USER and PASSWORD should match
  the database user you created in the previous step. 

  .. code-block:: python
     :emphasize-lines: 8,11

      DATABASES = {
        "default": {
          "ENGINE": "django.db.backends.postgresql",
          # Database name
          "NAME": "data_admin",
          # Role name when using md5 authentication.
          # Leave as an empty string when using peer or ident authencation.
          "USER": "frepple",
          # Role password when using md5 authentication.
          # Leave as an empty string when using peer or ident authencation.
          "PASSWORD": "frepple",
          # When using TCP sockets specify the hostname, the ip4 address or the ip6 address here.
          # Leave as an empty string to use Unix domain socket ("local" lines in pg_hba.conf).
          "HOST": "",
          # Specify the port number when using a TCP socket.
          "PORT": "",
          "OPTIONS": {},
          "CONN_MAX_AGE": 60,
          "TEST": {
            "NAME": "test_data_admin"  # Database name used when running the test suite.
            },
          "FILEUPLOADFOLDER": os.path.normpath(
            os.path.join(FREPPLE_LOGDIR, "data", "default")
            ),
          "SECRET_WEBTOKEN_KEY": SECRET_KEY,
          }
        }
        
* INSTALLED_APPS:

  This setting configures the apps that will be deployed on your web server. 
  
  The minimal content for this block is as follows. Notice the "example1" app
  at a specific place in the list. 
  
  .. code-block:: python
     :emphasize-lines: 7

      INSTALLED_APPS = (
          "django.contrib.auth",
          "django.contrib.contenttypes",
          "django.contrib.messages",
          "django.contrib.staticfiles",
          "data_admin.boot",
          "data_admin_examples.example1",   # <<< The example app 
          "data_admin.execute",
          "data_admin.common",
          "django_filters",
          "rest_framework",
          "django_admin_bootstrapped",
          "django.contrib.admin",
      )


.. _example_intialize:

Initialize the database
-----------------------

With the following commands we will create a database, build all database tables and load some sample data.

  .. code-block:: none

      >> frepplectl.py createdatabase
      
          Executing SQL statement: create database "data_admin" encoding = 'UTF8'

      
      >> frepplectl.py migrate

          Operations to perform:
            Apply all migrations: admin, auth, common, contenttypes, example1, execute
          Running migrations:
            Applying contenttypes.0001_initial... OK
            Applying contenttypes.0002_remove_content_type_name... OK
            Applying auth.0001_initial... OK
            Applying auth.0002_alter_permission_name_max_length... OK
            Applying auth.0003_alter_user_email_max_length... OK
            Applying auth.0004_alter_user_username_opts... OK
            Applying auth.0005_alter_user_last_login_null... OK
            Applying auth.0006_require_contenttypes_0002... OK
            Applying auth.0007_alter_validators_add_error_messages... OK
            Applying auth.0008_alter_user_username_max_length... OK
            Applying auth.0009_alter_user_last_name_max_length... OK
            Applying auth.0010_alter_group_name_max_length... OK
            Applying auth.0011_update_proxy_permissions... OK
            Applying common.0001_initial... OK
            Applying admin.0001_initial... OK
            Applying admin.0002_logentry_remove_auto_add... OK
            Applying admin.0003_logentry_add_action_flag_choices... OK
            Applying example1.0001_initial... OK
            Applying execute.0001_initial... OK      


      >> frepplectl.py loaddata example1
      
            Installed 29 object(s) from 1 fixture(s)
      

.. _example_runserver:

Run the web server
------------------

Now, we can run the web server and use data-admin from your browser.
If all goes well, you will see a message with the URL.

  .. code-block:: none

      >> frepplectl.py runserver
       
            INFO Watching for file changes with StatReloader
            Performing system checks...
    
            System check identified no issues (1 silenced).
            Django version 2.2.17, using settings 'data_admin.settings'
            Starting development server at http://127.0.0.1:8000/
            Quit the server with CTRL-BREAK.

You can now open your favorite browser on http://127.0.0.1:8000/.
A default user **admin** is created automatically with password **admin**.
