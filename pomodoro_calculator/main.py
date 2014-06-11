"""Calculate the number of Pomodori available within a time period.

Usage:
  get-pomodori [--from=<time>] [--break=<minutes>] [--long-break=<minutes>] <end-time>
  get-pomodori (-h | --help | --version)

Options:
  --version                   show program's version number and exit.
  -h, --help                  show this help message and exit.
  -f, --from=<time>           calculate available pomodori from this time [default: now].
  -b, --break=<minutes>       the amount of minutes between each pomodori [default: 5].
  -l, --long-break=<minutes>  the amount of mintues between every five pomodori [default: 15].
"""
from docopt import docopt


def main():
    docopt(__doc__, version='0.2')

if __name__ == '__main__':
    main()
