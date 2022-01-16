from typing import List

from solver_generators.base_generator import BaseGenerator
from solver_generators.word_comparisons import WordComparison


class SmallestBucketGenerator(BaseGenerator):
    def _find_guess(self, possible_guesses: List[str], valid_words: List[str]) -> str:
        """
        Return the guess whose largest bucket is the smallest out of any guess
        """
        min_largest_bucket = len(valid_words) + 1
        best_guess = possible_guesses[0]
        for guess in possible_guesses:
            buckets_data = WordComparison.split_into_pattern_match_groups(guess, valid_words)
            largest_bucket_size = max(len(word_list) for word_list in buckets_data.values())
            if min_largest_bucket > largest_bucket_size:
                min_largest_bucket = largest_bucket_size
                best_guess = guess

        return best_guess
