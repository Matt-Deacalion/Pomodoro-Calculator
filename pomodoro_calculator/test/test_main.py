import unittest
from datetime import datetime, timedelta
from itertools import islice

from pomodoro_calculator import PomodoroCalculator, humanise_seconds

from freezegun import freeze_time


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

    def test_create_timedelta_with_hours(self):
        """
        Does `_create_timedelta` work correctly with only hours provided?
        """
        self.assertEqual(
            self.calculator._create_timedelta('15'),
            timedelta(hours=15),
        )

    def test_create_timedelta_with_hours_and_minutes(self):
        """
        Does `_create_timedelta` work correctly with hours and minutes?
        """
        self.assertEqual(
            self.calculator._create_timedelta('15:30'),
            timedelta(hours=15, minutes=30),
        )

    def test_create_timedelta_with_hours_minutes_and_seconds(self):
        """
        Does `_create_timedelta` work correctly with hours, minutes and seconds?
        """
        self.assertEqual(
            self.calculator._create_timedelta('15:30:25'),
            timedelta(hours=15, minutes=30, seconds=25),
        )

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

        self.assertEqual(
            PomodoroCalculator(end='10:00', interval=True).end,
            datetime(2014, 1, 2, 1, 30),
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
            pomodoro._get_item(3600, 'pomodoro', 1),
            {
                'index': 1,
                'pomodori-index': 1,
                'type': 'pomodoro',
                'start': datetime(2014, 1, 1, 2, 1),
                'end': datetime(2014, 1, 1, 2, 26),
                'length': 1500,
            },
        )

        self.assertDictEqual(
            short_break._get_item(3600, 'short-break', 2),
            {
                'index': 2,
                'pomodori-index': 2,
                'type': 'short-break',
                'start': datetime(2014, 1, 1, 2, 1),
                'end': datetime(2014, 1, 1, 2, 6),
                'length': 300,
            },
        )

        self.assertDictEqual(
            long_break._get_item(3600, 'long-break', 3),
            {
                'index': 3,
                'pomodori-index': 2,
                'type': 'long-break',
                'start': datetime(2014, 1, 1, 2, 1),
                'end': datetime(2014, 1, 1, 2, 16),
                'length': 900,
            },
        )

    @freeze_time('2014-01-01 00:00:00')
    def test_pomodori_none(self):
        """
        Does the `pomodori_schedule` method return `None` if there's
        no time?
        """
        self.assertIsNone(
            PomodoroCalculator(end='00:05').pomodori_schedule()
        )

    @freeze_time('2014-01-01 00:00:00')
    def test_pomodori_single_pomodoro(self):
        """
        Does the `pomodori_schedule` method return a single Pomodoro if there's
        just enough time?
        """
        pomodori = PomodoroCalculator(end='00:26').pomodori_schedule()

        self.assertEqual(len(pomodori['segments']), 1)
        self.assertEqual(pomodori['segments'][0].get('type'), 'pomodoro')

    @freeze_time('2014-01-01 00:00:00')
    def test_pomodori_never_ends_with_break(self):
        """
        The list that the `pomodori_schedule` method returns can never end in a
        short or long break.
        """
        times = [
            '{:02d}:{:02d}'.format(h, m)
            for m in range(0, 60)
            for h in range(0, 24)
        ]

        for time in times:
            pomodori = PomodoroCalculator(end=time).pomodori_schedule()

            if pomodori:
                self.assertEqual(
                    pomodori['segments'][0].get('type'),
                    'pomodoro',
                )
                self.assertNotEqual(
                    pomodori['segments'][0].get('type'),
                    'short-break',
                )
                self.assertNotEqual(
                    pomodori['segments'][0].get('type'),
                    'long-break',
                )

    @freeze_time('2014-01-01 12:00:00')
    def test_pomodori(self):
        """
        Does the `pomodori_schedule` method return the correct Pomodori
        entities?
        """
        pomodori = PomodoroCalculator(end='14:50').pomodori_schedule()

        expected_segments = [
            (pomodori['segments'][-1]['start'], datetime(2014, 1, 1, 14, 19)),
            (pomodori['segments'][-1]['end'], datetime(2014, 1, 1, 14, 44)),
            (len([e for e in pomodori['segments'] if e['type'] == 'pomodoro']), 5),
            (len([e for e in pomodori['segments'] if e['type'] == 'short-break']), 3),
            (len([e for e in pomodori['segments'] if e['type'] == 'long-break']), 1),
        ]

        for expected_segment in expected_segments:
            self.assertEqual(expected_segment[0], expected_segment[1])

    @freeze_time('2014-01-01 12:00:00')
    def test_pomodori_meta_data(self):
        """
        Does the `pomodori_schedule` method return the correct meta
        data about the Pomodori entities?
        """
        pomodori = PomodoroCalculator(end='14:36').pomodori_schedule()

        del pomodori['segments']

        self.assertDictEqual(
            pomodori,
            {
                'end': datetime(2014, 1, 1, 14, 2),
                'start': datetime(2014, 1, 1, 12, 0),
                'seconds-per-pomodoro': 1500,
                'total-breaks': 3,
                'total-pomodori': 4,
                'total-rest-time': 900,
                'total-work-time': 6000,
            },
        )

    @freeze_time('2014-01-01 12:00:00')
    def test_pomodori_does_not_overflow(self):
        """
        The `pomodori_schedule` method should not return any entities that go
        past the time limit.
        """
        pomodori = PomodoroCalculator(end='15:00').pomodori_schedule()
        self.assertLess(
            pomodori['segments'][-1]['end'], datetime(2014, 1, 1, 15)
        )

    def test_pomodori_segment_generator(self):
        """
        Are 'segment' (Pomodori, short breaks and long breaks) strings
        generated correctly?
        """
        self.assertListEqual(
            list(islice(self.calculator.pomodori_segments(), 16)),
            [
                'pomodoro',
                'short-break',
                'pomodoro',
                'short-break',
                'pomodoro',
                'short-break',
                'pomodoro',
                'long-break',
                'pomodoro',
                'short-break',
                'pomodoro',
                'short-break',
                'pomodoro',
                'short-break',
                'pomodoro',
                'long-break',
            ]
        )

    def test_humanise_seconds(self):
        """
        Does the `humanise_seconds` utility function work correctly?
        """
        self.assertEqual(humanise_seconds(60), '1 minute')
        self.assertEqual(humanise_seconds(120), '2 minutes')
        self.assertEqual(humanise_seconds(65), '1 minute')
        self.assertEqual(humanise_seconds(3600), '1 hour')
        self.assertEqual(humanise_seconds(7200), '2 hours')
        self.assertEqual(humanise_seconds(7265), '2 hours, 1 minute')
