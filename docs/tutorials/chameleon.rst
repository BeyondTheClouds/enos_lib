*****************************
Provider::Openstack/Chameleon
*****************************

.. contents::
   :depth: 2

This tutorial will let you get started using |enoslib| and Openstack and/or Chameleon.
Chameleon provider is an Openstak provider specialization.

Here we present you the bare minimum to install the library with the required
dependencies.

.. hint::

   For a complete schema reference see :ref:`openstack-schema`

Installation
============

.. code-block:: bash

    # This will install the openstack clients
    $ pip install enoslib[chameleon]

.. note::

  It's a good practice to use a virtualenv or a python version manager like `pyenv`.


Openstack example
=================

The following reserve 2 nodes on the chameleon baremetal infrastructure.
Prior to the execution you must source your openrc file.

.. code-block:: bash

   $ source admin-rc.sh


You must also configure an access key in you project and replace with its name
in the following.


.. literalinclude:: chameleon/tuto_openstack.py
   :language: python
   :linenos:


.. note::

   Similarly to other provider the configuration can be generated
   programmatically instead of using a dict.



Chameleon example
=================

The following reserve 2 nodes on the chameleon baremetal infrastructure.
Prior to the execution you must source your openrc file.

.. code-block:: bash

   $ source CH-XXXXX.sh


You must also configure an access key in you project and replace with its name
in the following.


.. literalinclude:: chameleon/tuto_chameleonbaremetal.py
   :language: python
   :linenos:


.. note::

   Similarly to other provider the configuration can be generated
   programmatically instead of using a dict.


The result of the above code is the following:

.. image:: chameleon/result.png
