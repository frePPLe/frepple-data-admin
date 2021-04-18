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

The installation is straightforward with pip, the Python package manager:

.. code-block:: none

    pip3 install data-admin

Alternatively, you run from the source by cloning the git repository. In this
case, you need to install some Python packages yourself.

.. code-block:: none

    git clone https://github.com/frePPLe/frepple-data-admin.git data-admin
    
    cd data-admin
    
    pip3 install -r requirements.txt

Using a Python virtual environment is supported.


.. _install_dbuser:

Create a PostgreSQL database user
---------------------------------

Next, create a database user for data admin. From a psql prompt or 
pgadmin, you can do this with the following SQL command: 

.. code-block:: none

    create role frepple with login superuser password 'frepple';

The role name, password and privileges can be changed to your taste. The
above is just a quick default to get started with. 
