
.. |travis| image:: https://travis-ci.org/dry-python/dependencies.svg?branch=master
    :target: https://travis-ci.org/dry-python/dependencies

.. |codecov| image:: https://codecov.io/gh/dry-python/dependencies/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/dry-python/dependencies

.. |pyup| image:: https://pyup.io/repos/github/dry-python/dependencies/shield.svg
     :target: https://pyup.io/repos/github/dry-python/dependencies/

.. |codacy| image:: https://api.codacy.com/project/badge/Grade/ac9894ac09cc41028c3eb6fbc27126ad
    :target: https://www.codacy.com/app/dry-python/dependencies

.. |pypi| image:: https://img.shields.io/pypi/v/dependencies.svg
    :target: https://pypi.python.org/pypi/dependencies/

.. |docs| image:: https://readthedocs.org/projects/dependencies/badge/?version=latest
    :target: http://dependencies.readthedocs.io/en/latest/?badge=latest

.. image:: https://raw.githubusercontent.com/dry-python/brand/master/logo/dependencies.png

|travis| |codecov| |pyup| |codacy| |pypi| |docs|

----

Dependency Injection for Humans
===============================

Dependency Injection (or simply DI) is great technique.  By using it
you can organize responsibilities in you code base.  Define high level
policies and system behavior in one part.  Delegate control to low
level mechanisms from different part.  Simple and powerful.

With help of DI you can use different parts of you system
independently and combine their behavior really easy.

If you split logic and implementation into different classes, you will
see how pleasant it became to change your system.

This tiny library helps you to connect parts of your system i.e. to
inject low level implementation into high level behavior.

Example
=======

Dependency injection without ``dependencies``

.. code:: python

    robot = Robot(
        servo=Servo(amplifier=Amplifier()),
        controller=Controller(),
        settings=Settings(environment="production"),
    )

    robot.work()

Dependency injection with ``dependencies``

.. code:: python

    class Container(Injector):
        robot = Robot
        servo = Servo
        amplifier = Amplifier
        controller = Controller
        settings = Settings
        environment = "production"

    Container.robot.work()

Installation
============

Release version
---------------

Dependencies is available on PyPI - to install it just run::

    pip install -U dependencies

That's it!  Once installed, ``dependencies`` are available to use.
Import it and have fun.

Development version
-------------------

You can always install last development version directly from source
control::

    pip install -U git+https://github.com/dry-python/dependencies.git

Contents
========

.. toctree::
    :maxdepth: 2

    overview
    why
    usage
    proxies/index
    contrib/index
    implementation

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
