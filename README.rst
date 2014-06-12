===================
Pomodoro Calculator
===================
.. image:: https://travis-ci.org/Matt-Stevens/Pomodoro-Calculator.svg?branch=master
    :target: https://travis-ci.org/Matt-Stevens/Pomodoro-Calculator

Command line tool to calculate the number of Pomodori available between two points in time.

.. image:: https://raw.github.com/Matt-Stevens/Pomodoro-Calculator/screenshots/screenshot.png
    :alt: Pomodoro Calculator screenshot
    :align: center

Installation
------------
You can install pomodoro-calculator using pip::

    $ pip install pomodoro-calculator

Usage
-----
You can use the `get-pomodori` command from the shell to run the Pomodoro Calculator::

    $ get-pomodori --help

    Calculate the number of Pomodori available within a time period.

    Usage:
      get-pomodori [--from=<time>] [--break=<minutes>] [--long-break=<minutes>] <end-time>
      get-pomodori (-h | --help | --version)

    Options:
      --version                   show program's version number and exit.
      -h, --help                  show this help message and exit.
      -f, --from=<time>           calculate available Pomodori from this time [default: now].
      -b, --break=<minutes>       the amount of minutes between each Pomodori [default: 5].
      -l, --long-break=<minutes>  the amount of minutes between every four Pomodori [default: 15].

Licence
-------
Copyright © 2014 `Matt Deacalion Stevens`_, released under The `MIT License`_.

.. _Matt Deacalion Stevens: http://dirtymonkey.co.uk
.. _MIT License: http://deacalion.mit-license.org
