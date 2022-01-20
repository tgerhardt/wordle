from typing import List

from solver_generators.base_generator import BaseGenerator
from solver_generators.word_comparisons import WordComparison


class InformationGenerator(BaseGenerator):
    # This values were guessed based on rough ideas of information gain
    RESPONSE_VALUE_HEURISTIC = {
        WordComparison.MATCH_NONE: 1,  # A wrong guess for a letter removes options
        WordComparison.MATCH_PRESENCE: 5,  # After 5 guesses, we expect to get a hit in the word
        WordComparison.MATCH_POSITION: 15  # After guessing a letter in the word, it takes 2.5 more to determine place
    }

    @staticmethod
    def find_guess(possible_guesses: List[str], valid_words: List[str]) -> str:
        """
        Return the guess that gives the most information
        """
        most_information = 0
        most_information_guess = None
        for guess in possible_guesses:
            response = WordComparison.split_into_pattern_match_groups(guess, valid_words)

            # Calculate informaiton content
            information_value = 0
            for key, value in response.items():
                # Get the information value of the key (e.g. GYBGY is worth 41)
                key_information_value = 0
                for char in key:
                    key_information_value += InformationGenerator.RESPONSE_VALUE_HEURISTIC[char]

                # Multiply by the number of words in this bucket.
                # The more words in a high-value bucket, the better our score
                information_value += key_information_value * len(value)

            if information_value > most_information:
                most_information = information_value
                most_information_guess = guess

        return most_information_guess
