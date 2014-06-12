# coding=utf-8

"""Calculate the number of Pomodori available within a time period.

Usage:
  get-pomodori [--from=<time>] [--break=<minutes>] [--long-break=<minutes>] <end-time>
  get-pomodori (-h | --help | --version)

Options:
  --version                   show program's version number and exit.
  -h, --help                  show this help message and exit.
  -f, --from=<time>           calculate available Pomodori from this time [default: now].
  -b, --break=<minutes>       the amount of minutes between each Pomodori [default: 5].
  -l, --long-break=<minutes>  the amount of minutes between every four Pomodori [default: 15].
"""
from docopt import docopt
from pomodoro_calculator import PomodoroCalculator, __version__
from colorama import Fore, Style, init


def main():
    arguments = docopt(__doc__, version=__version__)

    calc = PomodoroCalculator(
        end=arguments['<end-time>'],
        start=arguments['--from'],
        short_break=int(arguments['--break']),
        long_break=int(arguments['--long-break']),
    )

    colours = {
        'pomodoro': Style.BRIGHT + Fore.RED,
        'short-break': Fore.BLUE,
        'long-break': Fore.CYAN,
    }

    init(autoreset=True)

    pomodori_count = 0

    for segment in calc.pomodori_schedule():
        line_dict = {}

        if segment['type'] == 'pomodoro':
            pomodori_count += 1

            line_dict['id'] = pomodori_count
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

    total = '{:>26} {:>2}'.format('Total Pomodori:', pomodori_count)
    print(Style.BRIGHT + Fore.WHITE + total)

if __name__ == '__main__':
    main()
