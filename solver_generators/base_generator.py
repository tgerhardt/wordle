from typing import List
from solver_generators.word_comparisons import WordComparison

class BaseGenerator(object):
    MODE_EASY = 'easy'  # Allow any word to be guessed
    MODE_HARD = 'hard'  # Require only valid words (based on the previous guesses) to be guessed

    MAX_DEPTH = 6  # The most guesses we'll have in a solver

    def __init__(self, mode: str, full_word_list: List[str]):
        """
        Initialize the class
        """
        self._mode = mode
        self._full_word_list = full_word_list

    @staticmethod
    def find_guess(possible_guesses: List[str], valid_words: List[str]) -> str:
        """
        Take in the possible guesses and determine the best one. Implemented in child classes
        """
        raise NotImplementedError

    def _recursively_generate_a_solver(self, possible_guesses: List[str], valid_words: List[str], depth: int) -> dict:
        """
        Generate a solver. A solver is a nested dictionary that can be used to guess a word
        """
        # Determine the guess
        guess = self.find_guess(possible_guesses, valid_words)

        # Use the guess to split apart the remaining words
        groupings = WordComparison.split_into_pattern_match_groups(guess, valid_words)
        if 'GGGGG' in groupings:
            del groupings['GGGGG']

        result = {
            'guess': guess
        }
        if depth == self.MAX_DEPTH:
            # We're at the end
            result['branches'] = groupings
            return result
        else:
            # Recurse
            result['branches'] = {}
            for pattern, words in groupings.items():
                if self._mode == self.MODE_EASY:
                    # We can guess anything
                    sub_results = self._recursively_generate_a_solver(possible_guesses, words, depth + 1)
                else:
                    # We can only guess valid words
                    sub_results = self._recursively_generate_a_solver(words, words, depth + 1)
                result['branches'][pattern] = sub_results
        return result

    def generate_solver(self):
        """
        Generate a solver. A solver is a nested dictionary that can be used to guess a word
        """
        return self._recursively_generate_a_solver(self._full_word_list, self._full_word_list, 1)
