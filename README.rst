===================
Pomodoro Calculator
===================
.. image:: https://travis-ci.org/Matt-Deacalion/Pomodoro-Calculator.svg?branch=master&new
    :target: https://travis-ci.org/Matt-Deacalion/Pomodoro-Calculator
    :alt: Build Status
.. image:: https://coveralls.io/repos/Matt-Deacalion/Pomodoro-Calculator/badge.png?branch=master&new
    :target: https://coveralls.io/r/Matt-Deacalion/Pomodoro-Calculator?branch=master
    :alt: Test Coverage
.. image:: https://img.shields.io/pypi/dw/pomodoro-calculator.svg
    :target: https://pypi.python.org/pypi/pomodoro-calculator/
    :alt: Downloads
.. image:: https://img.shields.io/pypi/v/pomodoro-calculator.svg
    :target: https://pypi.python.org/pypi/pomodoro-calculator/
    :alt: Latest Version
.. image:: https://img.shields.io/pypi/wheel/pomodoro-calculator.svg
    :target: https://pypi.python.org/pypi/pomodoro-calculator/
    :alt: Wheel Status
.. image:: https://img.shields.io/badge/license-MIT-blue.svg
    :target: https://pypi.python.org/pypi/pomodoro-calculator/
    :alt: License

A pretty command line tool to calculate the number of Pomodori available between
two points in time.

.. image:: https://raw.github.com/Matt-Deacalion/Pomodoro-Calculator/screenshots/screenshot.png
    :alt: Pomodoro Calculator screenshot
    :align: center

Installation
------------
You can install pomodoro-calculator using pip::

    $ pip install pomodoro-calculator

Usage
-----
Use the `get-pomodori` command from the shell to run the Pomodoro Calculator::

    $ get-pomodori --help

    Calculate the number of Pomodori available within a time period.

    Usage:
      get-pomodori [--from=<time>] [--break=<minutes>] [--long-break=<minutes>] [-i] <end-time>
      get-pomodori (-h | --help | --version)

    Options:
      --version                   show program's version number and exit.
      -h, --help                  show this help message and exit.
      -i                          specify that <endtime> will be used as delta time interval.
      -f, --from=<time>           calculate available Pomodori from this time [default: now].
      -b, --break=<minutes>       the amount of minutes between each Pomodori [default: 5].
      -l, --long-break=<minutes>  the amount of minutes between every four Pomodori [default: 15].
      -p, --pomodoro=<minutes>    the amount of minutes for every pomodoro session [default: 25].
      -g, --group=<pomodori>      the amount of pomodori before a long break [default: 4].

Licence
-------
Copyright © 2015 `Matt Deacalion Stevens`_, released under The `MIT License`_.

.. _Matt Deacalion Stevens: http://dirtymonkey.co.uk
.. _MIT License: http://deacalion.mit-license.org
