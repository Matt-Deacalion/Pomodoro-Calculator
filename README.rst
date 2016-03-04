===================
Pomodoro Calculator
===================
A pretty command line tool to calculate the number of Pomodori available between
two points in time.

.. image:: https://raw.github.com/Matt-Deacalion/Pomodoro-Calculator/master/screenshot.png
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
      get-pomodori [options] <end-time>
      get-pomodori (-h | --help | --version)

    Options:
      --version                   show program's version number and exit.
      -h, --help                  show this help message and exit.
      -i, --interval              specify that the end time is a time interval, not a time of day.
      -f, --from=<time>           calculate available Pomodori from this time [default: now].
      -b, --break=<minutes>       the amount of minutes between each Pomodori [default: 5].
      -l, --long-break=<minutes>  the amount of minutes between every four Pomodori [default: 15].
      -p, --pomodoro=<minutes>    the amount of minutes for every pomodoro session [default: 25].
      -g, --group=<pomodori>      the amount of pomodori before a long break [default: 4].
      -j, --json                  output the pomodori schedule in JSON format.
      -n, --nocolour              do not colourise the output.

Licence
-------
Copyright © 2016 `Matt Deacalion Stevens`_, released under The `MIT License`_.

.. _Matt Deacalion Stevens: http://dirtymonkey.co.uk
.. _MIT License: http://deacalion.mit-license.org
