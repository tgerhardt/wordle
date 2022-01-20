from typing import List

from solver_generators.base_generator import BaseGenerator


class AlphabeticalGenerator(BaseGenerator):
    @staticmethod
    def find_guess(possible_guesses: List[str], valid_words: List[str]) -> str:
        """
        Return the first alphabetical guess
        """
        return min(possible_guesses)
