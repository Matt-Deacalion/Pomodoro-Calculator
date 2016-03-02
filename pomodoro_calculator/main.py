# coding=utf-8

"""Calculate the number of Pomodori available within a time period.

Usage:
  get-pomodori [--pomodoro=<time>] [--from=<time>] [--break=<minutes>]
               [--long-break=<minutes>] [--group=<pomodori>] [--interval] <end-time>
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
"""
from __future__ import print_function

import sys

from colorama import Fore, Style, init
from docopt import docopt

from pomodoro_calculator import PomodoroCalculator, __version__

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO


def report_output(schedule):
    """
    Takes a Pomodori schedule and returns a pretty, report style
    string that can be printed to the terminal or piped elsewhere.
    """
    colours = {
        'pomodoro': Style.BRIGHT + Fore.RED,
        'short-break': Fore.BLUE,
        'long-break': Fore.CYAN,
    }

    output = StringIO()

    # backup previous standard output, redirect new one to our string
    stdout = sys.stdout
    sys.stdout = output

    init(autoreset=True)

    for segment in schedule['segments']:
        line_dict = {}

        if segment['type'] == 'pomodoro':
            line_dict['id'] = segment['pomodori-index']
            line_dict['name'] = 'Pomodoro'

        elif segment['type'] == 'short-break':
            line_dict['id'] = ''
            line_dict['name'] = 'short break'

        else:
            line_dict['id'] = ''
            line_dict['name'] = 'long break'

        line_dict['start'] = segment['start'].strftime('%H:%M')
        line_dict['end'] = segment['end'].strftime('%H:%M')

        line = "{id:>2} {name:<12} {start} ⇾ {end}".format(**line_dict)
        print(colours[segment['type']] + line)

    total = '{:>26} {:>2}'.format(
        'Total Pomodori:',
        schedule['total-pomodori'],
    )
    print(Style.BRIGHT + Fore.WHITE + total)

    hours = round(
        schedule['total-pomodori'] * schedule['seconds-per-pomodoro'] / 60 / 60,
        1,
    )
    total = '{:>26} {:>2}h'.format('Total Work:', hours)
    print(Style.BRIGHT + Fore.WHITE + total)

    # restore the previous standard output
    sys.stdout = stdout

    return output.getvalue()


def main():
    arguments = docopt(__doc__, version=__version__)

    calc = PomodoroCalculator(
        end=arguments['<end-time>'],
        start=arguments['--from'],
        pomodoro_length=int(arguments['--pomodoro']),
        group_length=int(arguments['--group']),
        short_break=int(arguments['--break']),
        long_break=int(arguments['--long-break']),
        interval=arguments['--interval'],
    )

    print(report_output(calc.pomodori_schedule()), end='')
    sys.stdout.flush()

if __name__ == '__main__':
    main()
