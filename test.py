from datetime import datetime
from nose.tools import eq_, raises
import pomodoro_count


@raises(pomodoro_count.ArgumentError)
def test_dates_valid():
    """
    Only datetime or datetime derived objects are accepted.
    """
    pomodoro_count.get_pomodoros(1, 2)


@raises(pomodoro_count.ArgumentError)
def test_end_date_after_start():
    """
    The end datetime must always be in the future relative to the start.
    """
    pomodoro_count.get_pomodoros(datetime(2000, 1, 2), datetime(2000, 1, 1))


def test_pomodoro_count():
    """
    How many pomodoros are possible in a time period.
    """
    return eq_(pomodoro_count.get_pomodoros(datetime(2000, 1, 1), datetime(2000, 1, 2)), 48)


def test_pomodoro_count_with_rests():
    """
    How many pomodoros are possible in a time period, including a rest between each.
    """
    return eq_(pomodoro_count.get_pomodoros(datetime(2000, 1, 1), datetime(2000, 1, 2), 60 * 30), 24)
