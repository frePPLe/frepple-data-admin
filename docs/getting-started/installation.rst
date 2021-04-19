============
Installation
============

* :ref:`install_prerequisites`
* :ref:`install_pip`
* :ref:`install_dbuser`


.. _install_prerequisites:

Prerequisites
-------------

You will need:

- Python from https://www.python.org/ (any version >= 3.6)

- PostgreSQL from https://www.postgresql.org/ (any version >= 9)


.. _install_pip:

Install the Python package
--------------------------

Download the source code from github https://github.com/frePPLe/frepple-data-admin
into a local folder on your machine.

Open a command prompt in that folder and install the third party Python
packages data-admin depends on. Using a Python virtual environment is supported. 

.. code-block:: none
    
    pip3 install -r requirements.txt


.. _install_dbuser:

Create a PostgreSQL database user
---------------------------------

Next, create a database user for data admin. From a psql prompt or 
pgadmin, you can do this with the following SQL command: 

.. code-block:: none

    create role frepple with login superuser password 'frepple';

The role name, password and privileges can be changed to your taste. The
above is just a quick default to get started with. 
