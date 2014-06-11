import datetime
from itertools import cycle


class PomodoroCalculator:
    """
    Calculates the number of pomodoros available in an amount of time.
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

    def pomodori(self):
        """
        Returns a list of dicts of Pomodori and the related breaks inbetween.
        """
        pomodori = []
        iterations = 0
        seconds = self.total_seconds

        if seconds < self.pomodoro_length:
            return []

        while seconds > 0:
            # zero and even numbers are always Pomodori
            if iterations % 2 == 0 or iterations == 0:
                pomodori.append(self._get_item(seconds, 'pomodoro'))
                seconds -= self.pomodoro_length
            else:
                quotient, remainder = divmod(iterations+1, 4)

                # if the quotient is even and the remainder is zero, then we
                # are just after a fourth Pomodori and should add a long break
                if quotient % 2 == 0 and remainder == 0:
                    pomodori.append(self._get_item(seconds, 'long-break'))
                    seconds -= self.long_break_seconds
                # otherwise, we're at a short break
                else:
                    pomodori.append(self._get_item(seconds, 'short-break'))
                    seconds -= self.short_break_seconds

            iterations += 1

        # remove breaks that are not followed by a Pomodoro
        if pomodori[-1].get('type') != 'pomodoro':
            del pomodori[-1]

        return pomodori
