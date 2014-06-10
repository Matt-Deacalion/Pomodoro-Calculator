import unittest
from datetime import datetime
from freezegun import freeze_time
from pomodoro_calculator import PomodoroCalculator


class PomodoroTest(unittest.TestCase):

    def setUp(self):
        self.calculator = PomodoroCalculator(end='15:00')

    def test_retriever_class_exists(self):
        """
        Does the `PomodoroCalculator` class exist?
        """
        self.assertTrue('PomodoroCalculator' in globals())

    @freeze_time('2014-01-01 00:00:00')
    def test_create_datetime_with_hours(self):
        """
        Does `_create_datetime` work correctly with only hours provided?
        """
        self.assertEqual(
            self.calculator._create_datetime('15'),
            datetime(2014, 1, 1, 15),
        )

    @freeze_time('2014-01-01 00:00:00')
    def test_create_datetime_with_hours_and_minutes(self):
        """
        Does `_create_datetime` work correctly with hours and minutes?
        """
        self.assertEqual(
            self.calculator._create_datetime('15:30'),
            datetime(2014, 1, 1, 15, 30),
        )

    @freeze_time('2014-01-01 00:00:00')
    def test_create_datetime_with_hours_minutes_and_seconds(self):
        """
        Does `_create_datetime` work correctly with hours, minutes and seconds?
        """
        self.assertEqual(
            self.calculator._create_datetime('15:30:25'),
            datetime(2014, 1, 1, 15, 30, 25),
        )

    @freeze_time('2014-01-02 00:00:00')
    def test_create_datetime_with_different_day(self):
        """
        Does `_create_datetime` add another day is `tomorrow` is passed?
        """
        self.assertEqual(
            self.calculator._create_datetime('15:30:25', tomorrow=True),
            datetime(2014, 1, 3, 15, 30, 25),
        )

    def test_compare_times(self):
        """
        Does `_compare_times` work correctly?
        """
        times = [
            ('3', '5'),
            ('03', '05'),
            ('5:30', '6:30'),
            ('05:0', '06:0'),
            ('05:01', '06:00'),
            ('05:01:05', '06:00:20'),
            ('05:01:5', '06:00:2'),
        ]

        for t in times:
            self.assertFalse(self.calculator._compare_times(t[0], t[1]))
            self.assertTrue(self.calculator._compare_times(t[1], t[0]))

    @freeze_time('2014-01-01 15:30:00')
    def test_start_time_initialisation(self):
        """
        Does the `start` attribute initialise properly?
        """
        self.assertEqual(
            PomodoroCalculator(end='18:30').start,
            datetime(2014, 1, 1, 15, 30),
        )

        self.assertEqual(
            PomodoroCalculator(end='18:30', start='16:30').start,
            datetime(2014, 1, 1, 16, 30),
        )

    @freeze_time('2014-01-01 15:30:00')
    def test_end_time_initialisation(self):
        """
        Does the `end` attribute initialise properly?
        """
        self.assertEqual(
            PomodoroCalculator(end='18:30').end,
            datetime(2014, 1, 1, 18, 30),
        )

        self.assertEqual(
            PomodoroCalculator(end='18:30', start='19:30').end,
            datetime(2014, 1, 2, 18, 30),
        )

    def test_short_break_seconds(self):
        """
        Does the `short_break_seconds` property work correctly?
        """
        calculator = PomodoroCalculator(end='18:00', short_break=10)

        self.assertEqual(self.calculator.short_break_seconds, 5 * 60)
        self.assertEqual(calculator.short_break_seconds, 10 * 60)

    def test_long_break_seconds(self):
        """
        Does the `long_break_seconds` property work correctly?
        """
        calculator = PomodoroCalculator(end='18:00', long_break=10)

        self.assertEqual(self.calculator.long_break_seconds, 15 * 60)
        self.assertEqual(calculator.long_break_seconds, 10 * 60)

    def test_total_seconds(self):
        """
        Does the `total_seconds` property work correctly?
        """
        calculator = PomodoroCalculator(end='18:00', start='18:15')
        self.assertEqual(calculator.long_break_seconds, 15 * 60)

    @freeze_time('2014-01-01 00:00:00')
    def test_get_item(self):
        """
        Does the `_get_item` method work correctly?
        """
        pomodoro = PomodoroCalculator(end='03:00')
        short_break = PomodoroCalculator(end='03:00')
        long_break = PomodoroCalculator(end='03:00')

        self.assertDictEqual(
            pomodoro._get_item(3600, 'pomodoro'),
            {
                'type': 'pomodoro',
                'start': datetime(2014, 1, 1, 2),
                'end': datetime(2014, 1, 1, 2, 25),
            },
        )

        self.assertDictEqual(
            short_break._get_item(3600, 'short-break'),
            {
                'type': 'short-break',
                'start': datetime(2014, 1, 1, 2),
                'end': datetime(2014, 1, 1, 2, 5),
            },
        )

        self.assertDictEqual(
            long_break._get_item(3600, 'long-break'),
            {
                'type': 'long-break',
                'start': datetime(2014, 1, 1, 2),
                'end': datetime(2014, 1, 1, 2, 15),
            },
        )
