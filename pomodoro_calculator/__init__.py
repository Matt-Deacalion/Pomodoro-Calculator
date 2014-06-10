import datetime


class PomodoroCalculator:
    """
    Calculates the number of pomodoros available in an amount of time.
    """
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
