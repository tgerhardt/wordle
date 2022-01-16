from typing import List

from solver_generators.base_generator import BaseGenerator


class AlphabeticalGenerator(BaseGenerator):
    def _find_guess(self, possible_guesses: List[str], valid_words: List[str]) -> str:
        """
        Return the first alphabetical guess
        """
        return min(possible_guesses)
