from collections import defaultdict
from typing import Dict, List

class WordComparison(object):
    MATCH_NONE = "B"  # Black
    MATCH_PRESENCE = "Y"  # Yellow
    MATCH_POSITION = "G"  # Green

    MISS = MATCH_NONE * 5

    @staticmethod
    def word_match(guess: str, answer: str) -> str:
        """
        Take in two words and return a tuple. Each position in the tuple corresponds
        to a letter in the guess word and the value is the match type
        (none, presence, or position)
        """
        results = [WordComparison.MATCH_NONE] * len(guess)

        # Loop over the characters and split the letters into two groups:
        # position matches and other letters. We'll compare the other letters after
        other_guess_letters = defaultdict(int)
        other_answer_letters = defaultdict(int)
        for index, (guess_char, answer_char) in enumerate(zip(guess, answer)):
            if guess_char == answer_char:
                results[index] = WordComparison.MATCH_POSITION
            else:
                other_guess_letters[guess_char] += 1
                other_answer_letters[answer_char] += 1

        # Determine the overlap in the remaining characters
        overlap_char_counts = {}
        for char, count in other_guess_letters.items():
            overlap_char_counts[char] = min(other_answer_letters[char], count)

        # Loop over the guess word. For every letter that isn't already in the right
        # position, determine if it appears in the overlapping letters
        for index, guess_char in enumerate(guess):
            if results[index] == WordComparison.MATCH_NONE:
                if overlap_char_counts.get(guess_char) > 0:
                    results[index] = WordComparison.MATCH_PRESENCE
                    overlap_char_counts[guess_char] -= 1

        return "".join(results)

    @staticmethod
    def split_into_pattern_match_groups(guess: str, word_list: List[str]) -> Dict[str, List[str]]:
        """
        Given the guess and remaining valid words, break them into match pattern groups
        """
        match_pattern_groups = defaultdict(list)
        for answer in word_list:
            match_pattern_groups[WordComparison.word_match(guess, answer)].append(answer)
        return dict(match_pattern_groups)
