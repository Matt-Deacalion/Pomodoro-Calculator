# coding=utf-8

"""Calculate the number of Pomodori available within a time period.

Usage:
  get-pomodori [--pomodoro=<time>] [--from=<time>] [--break=<minutes>] [--long-break=<minutes>]
               [--group=<pomodori>] [--interval] [--json] [--nocolour] <end-time>
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
"""
from __future__ import print_function

import json
from datetime import datetime

from colorama import Fore, Style, init
from docopt import docopt
from pomodoro_calculator import (PomodoroCalculator, __version__,
                                 humanise_seconds)


class DateTimeEncoder(json.JSONEncoder):
    """
    Subclassed so we can encode `datetime` instances.
    """
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()

        return json.JSONEncoder.default(self, obj)


def report_output(schedule, no_colour=False):
    """
    Takes a Pomodori schedule and returns a pretty, report style
    string that can be printed to the terminal or piped elsewhere.
    """
    lines = []
    colours = {
        'pomodoro': '' if no_colour else Style.BRIGHT + Fore.RED,
        'short-break': '' if no_colour else Fore.BLUE,
        'long-break': '' if no_colour else Fore.CYAN,
        'total': '' if no_colour else Style.BRIGHT + Fore.WHITE,
    }

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

        line = '{id:>2} {name:<12} {start} ⇾ {end}'.format(**line_dict)
        lines.append(colours[segment['type']] + line)

    total = '\n{:>18} {}'.format(
            'Total Pomodori:',
            schedule['total-pomodori'],
    )
    lines.append(colours['total'] + total)

    total = '{:>18} {}'.format(
        'Total Work:',
        humanise_seconds(
            schedule['total-pomodori'] * schedule['seconds-per-pomodoro'],
        ),
    )
    lines.append(colours['total'] + total)

    return '\n'.join(lines)


def main():
    arguments = docopt(__doc__, version=__version__)

    schedule = PomodoroCalculator(
        end=arguments['<end-time>'],
        start=arguments['--from'],
        pomodoro_length=int(arguments['--pomodoro']),
        group_length=int(arguments['--group']),
        short_break=int(arguments['--break']),
        long_break=int(arguments['--long-break']),
        interval=arguments['--interval'],
    ).pomodori_schedule()

    if schedule is None:
        print('Oops, something went wrong! We need more time for our Pomodoros.')
        return

    if arguments['--json']:
        print(json.dumps(schedule, cls=DateTimeEncoder))
    else:
        print(report_output(schedule, arguments['--nocolour']))


if __name__ == '__main__':
    main()
