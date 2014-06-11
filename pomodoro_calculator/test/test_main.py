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
                'time': 1500,
            },
        )

        self.assertDictEqual(
            short_break._get_item(3600, 'short-break'),
            {
                'type': 'short-break',
                'start': datetime(2014, 1, 1, 2),
                'end': datetime(2014, 1, 1, 2, 5),
                'time': 300,
            },
        )

        self.assertDictEqual(
            long_break._get_item(3600, 'long-break'),
            {
                'type': 'long-break',
                'start': datetime(2014, 1, 1, 2),
                'end': datetime(2014, 1, 1, 2, 15),
                'time': 900,
            },
        )

    @freeze_time('2014-01-01 00:00:00')
    def test_pomodori_empty(self):
        """
        Does the `pomodori_schedule` method return an empty list if there's no
        time?
        """
        self.assertListEqual(
            PomodoroCalculator(end='00:05').pomodori_schedule(),
            [],
        )

    @freeze_time('2014-01-01 00:00:00')
    def test_pomodori_single_pomodoro(self):
        """
        Does the `pomodori_schedule` method return a single Pomodoro if there's
        just enough time?
        """
        pomodori = PomodoroCalculator(end='00:25').pomodori_schedule()

        self.assertEqual(len(pomodori), 1)
        self.assertEqual(pomodori[0].get('type'), 'pomodoro')

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
                self.assertEqual(pomodori[0].get('type'), 'pomodoro')
                self.assertNotEqual(pomodori[0].get('type'), 'short-break')
                self.assertNotEqual(pomodori[0].get('type'), 'long-break')

    @freeze_time('2014-01-01 12:00:00')
    def test_pomodori(self):
        """
        Does the `pomodori_schedule` method return the correct Pomodori
        entities?
        """
        pomodori = PomodoroCalculator(end='14:35').pomodori_schedule()

        expected = [
            (pomodori[-1]['start'], datetime(2014, 1, 1, 14, 10)),
            (pomodori[-1]['end'], datetime(2014, 1, 1, 14, 35)),
            (len([e for e in pomodori if e['type'] == 'pomodoro']), 5),
            (len([e for e in pomodori if e['type'] == 'short-break']), 3),
            (len([e for e in pomodori if e['type'] == 'long-break']), 1),
        ]

        for expectation in expected:
            self.assertEqual(expectation[0], expectation[1])

    @freeze_time('2014-01-01 12:00:00')
    def test_pomodori_does_not_overflow(self):
        """
        The `pomodori_schedule` method should not return any entities that go
        past the time limit.
        """
        pomodori = PomodoroCalculator(end='15:00').pomodori_schedule()
        self.assertLess(pomodori[-1]['end'], datetime(2014, 1, 1, 15))

    def test_pomodori_segment_generator(self):
        """
        Are 'segment' (Pomodori, short breaks and long breaks) strings
        generated correctly?
        """
        segments = []
        i = 0

        for segment in self.calculator.pomodori_segments():
            segments.append(segment)
            i += 1

            if i == 16:
                break

        self.assertListEqual(
            segments,
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
