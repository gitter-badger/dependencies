
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
    :target: https://dependencies.readthedocs.io/en/latest/?badge=latest

.. image:: https://raw.githubusercontent.com/dry-python/brand/master/logo/dependencies.png

|travis| |codecov| |pyup| |codacy| |pypi| |docs|

----

Dependency Injection for Humans
===============================

- `Source Code`_
- `Issue Tracker`_
- `Documentation`_

Installation
------------

All released versions are hosted on the Python Package Index.  You can
install this package with following command.

.. code:: bash

    pip install dependencies

Usage
-----

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

License
-------

Dependencies library is offered under the two clause BSD license.

.. _source code: https://github.com/dry-python/dependencies
.. _issue tracker: https://github.com/dry-python/dependencies/issues
.. _documentation: https://dependencies.readthedocs.io/en/latest/
