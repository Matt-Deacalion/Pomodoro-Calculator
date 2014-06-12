"""
Command line tool to calculate the number of
Pomodori available between two points in time.
"""
__author__ = 'Matt Deacalion Stevens'
__version__ = '0.3.1'

import datetime
from itertools import cycle


class PomodoroCalculator:
    """
    Calculates the number of Pomodori available in an amount of time.
    """
    pomodoro_length = 25 * 60

    def __init__(self, end, start='now', short_break=5, long_break=15):
        if start == 'now':
            start = datetime.datetime.now().strftime('%H:%M:%S')

        # if the end time is earlier than the start, overlap to the next day
        if self._compare_times(start, end):
            self.end = self._create_datetime(end, tomorrow=True)
        else:
            self.end = self._create_datetime(end)

        self.start = self._create_datetime(start)
        self.short_break = short_break
        self.long_break = long_break

    @property
    def short_break_seconds(self):
        """
        Returns `short_break` in seconds.
        """
        return self.short_break * 60

    @property
    def long_break_seconds(self):
        """
        Returns `long_break` in seconds.
        """
        return self.long_break * 60

    @property
    def total_seconds(self):
        """
        Return the total time span in seconds.
        """
        delta = self.end - self.start
        return int(delta.total_seconds())

    def _compare_times(self, a, b):
        """
        Returns True if the time string `a` is later than `b`.
        """
        return [int(i) for i in a.split(':')] > [int(i) for i in b.split(':')]

    def _create_datetime(self, time_string, tomorrow=False):
        """
        Takes a string in the format of 'HH:MM:SS' and returns a datetime. If
        `tomorrow` is True it adds another day to the result.
        """
        replace_args = dict(zip(
            ['hour', 'minute', 'second'],
            [int(unit) for unit in time_string.split(':')],
        ))

        date = datetime.datetime.now().replace(**replace_args)

        if tomorrow:
            date += datetime.timedelta(days=1)

        return date

    def _get_item(self, offset, item_type):
        """
        Returns one of three types of Pomodori entities. A short break, a long
        break or the Pomodoro itself. The returned dict also contains the
        start and end datetimes.
        """
        types = {
            'short-break': self.short_break_seconds,
            'long-break': self.long_break_seconds,
            'pomodoro': self.pomodoro_length,
        }

        start = self.end - datetime.timedelta(seconds=offset)
        end = start + datetime.timedelta(seconds=types[item_type])

        return {
            'type': item_type,
            'start': start,
            'end': end,
            'time': int((end - start).total_seconds()),
        }

    def pomodori_segments(self):
        """
        Generate Pomodori along with the short and long breaks in between.

        Credit: http://codereview.stackexchange.com/questions/53970
        """

        # every fourth Pomodori precedes a long break,
        # all others have short breaks following them
        return cycle(
            ['pomodoro', 'short-break'] * 3 + ['pomodoro', 'long-break'],
        )

    def pomodori_schedule(self):
        """
        Returns a Pomodori schedule, which is a list consisting of Pomodori
        segments (Pomodoro, short break or long break) in chronological order.

        Credit: http://codereview.stackexchange.com/questions/53970
        """
        available_time = self.total_seconds
        segments = []

        if available_time < self.pomodoro_length:
            return []

        for segment_name in self.pomodori_segments():
            segment = self._get_item(available_time, segment_name)

            if segment['time'] > available_time:
                break

            available_time -= segment['time']
            segments.append(segment)

        if segments and segments[-1]['type'].endswith('break'):
            segments.pop()

        return segments
