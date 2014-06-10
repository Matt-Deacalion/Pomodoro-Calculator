import unittest
from pomodoro_calculator import PomodoroCalculator


class PomodoroTest(unittest.TestCase):

    def test_retriever_class_exists(self):
        """
        Does the `PomodoroCalculator` class exist?
        """
        self.assertTrue('PomodoroCalculator' in globals())
