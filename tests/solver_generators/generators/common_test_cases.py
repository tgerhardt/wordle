import unittest
from typing import List

class BaseTestGeneratorWrapper:
    class BaseTestGenerator(unittest.TestCase):
        GENERATOR_CLASS = None

        FIND_GUESS_EASY_FLOWN = None

        def setUp(self):
            self.maxDiff = None  # Let us see the totality of the problem

        def _run_find_guess_test(self, possible_guesses: List[str], valid_words: List[str], expected_guess: str):
            """
            Run a find_guess test
            """
            guess = self.GENERATOR_CLASS.find_guess(possible_guesses, valid_words)
            self.assertEqual(expected_guess, guess)

        def test_find_guess_easy_flown(self):
            """
            A test to see if the solver will choose "flown" so we know which of the valid words it could be
            """
            possible_guesses = ['aahed', 'flown', 'sofar', 'solar', 'sonar', 'sowar']
            valid_words = ['sofar', 'solar', 'sonar', 'sowar']
            self._run_find_guess_test(possible_guesses, valid_words, self.FIND_GUESS_EASY_FLOWN)
