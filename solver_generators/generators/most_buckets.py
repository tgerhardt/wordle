from typing import List

from solver_generators.base_generator import BaseGenerator
from solver_generators.word_comparisons import WordComparison


class MaxBucketsGenerator(BaseGenerator):
    @staticmethod
    def find_guess(possible_guesses: List[str], valid_words: List[str]) -> str:
        """
        Return the guess that creates the most possible responses
        """
        max_buckets = 0
        max_bucket_guess = None
        for guess in possible_guesses:
            buckets = len(WordComparison.split_into_pattern_match_groups(guess, valid_words))
            if buckets > max_buckets:
                max_buckets = buckets
                max_bucket_guess = guess

        return max_bucket_guess
