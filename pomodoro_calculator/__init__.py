import datetime


class PomodoroCalculator:
    """
    Calculates the number of pomodoros available in an amount of time.
    """
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
            date + datetime.timedelta(days=1)

        return date
