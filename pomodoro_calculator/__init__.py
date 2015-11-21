"""
A pretty command line tool to calculate the number
of Pomodori available between two points in time.
"""
__author__ = 'Matt Deacalion Stevens'
__version__ = '0.3.9'

import datetime
from itertools import cycle


class PomodoroCalculator:
    """
    Calculates the number of Pomodori available in an amount of time.
    """
    def __init__(self, end, start='now', short_break=5, long_break=15,
                 pomodoro_length=25, group_length=4, interval=False):
        self.pomodoro_length_seconds = pomodoro_length * 60

        if start == 'now':
            self.start = datetime.datetime.now()
        else:
            self.start = self._create_datetime(start)

        if interval:
            self.end = self.start + self._create_timedelta(end)
        else:
            self.end = self._create_datetime(end)

            # if the end time is earlier than the start,
            # overlap to the next day
            if self.end.time() < self.start.time():
                self.end += datetime.timedelta(days=1)

        self.group_length = group_length
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

    def _create_timedelta(self, time_string):
        """
        Takes a string in the format of 'HH:MM:SS' and returns a timedelta.
        """
        args = dict(zip(
            ['hours', 'minutes', 'seconds'],
            [int(unit) for unit in time_string.split(':')],
        ))

        return datetime.timedelta(**args)

    def _create_datetime(self, time_string):
        """
        Takes a string in the format of 'HH:MM:SS' and returns a datetime.
        """
        args = dict(zip(
            ['hour', 'minute', 'second'],
            [int(unit) for unit in time_string.split(':')],
        ))

        return datetime.datetime.now().replace(**args)

    def _get_item(self, offset, item_type):
        """
        Returns one of three types of Pomodori entities. A short break, a long
        break or the Pomodoro itself. The returned dict also contains the
        start and end datetimes.
        """
        types = {
            'short-break': self.short_break_seconds,
            'long-break': self.long_break_seconds,
            'pomodoro': self.pomodoro_length_seconds,
        }

        start = self.end - datetime.timedelta(seconds=offset)
        end = start + datetime.timedelta(seconds=types[item_type])

        return {
            'type': item_type,
            'start': start,
            'end': end,
            'time': int((end - start).total_seconds()),
        }

    def pomodori_segments(self, group_length=4):
        """
        Generate Pomodori along with the short and long breaks in between.

        Credit: http://codereview.stackexchange.com/questions/53970
        """

        # every fourth Pomodori precedes a long break,
        # all others have short breaks following them
        return cycle(
            ['pomodoro', 'short-break'] * (group_length - 1) + ['pomodoro', 'long-break'],
        )

    def pomodori_schedule(self):
        """
        Returns a Pomodori schedule, which is a list consisting of Pomodori
        segments (Pomodoro, short break or long break) in chronological order.

        Credit: http://codereview.stackexchange.com/questions/53970
        """
        available_time = self.total_seconds
        segments = []

        if available_time < self.pomodoro_length_seconds:
            return []

        for segment_name in self.pomodori_segments(self.group_length):
            segment = self._get_item(available_time, segment_name)

            if segment['time'] > available_time:
                break

            available_time -= segment['time']
            segments.append(segment)

        if segments and segments[-1]['type'].endswith('break'):
            segments.pop()

        return segments
