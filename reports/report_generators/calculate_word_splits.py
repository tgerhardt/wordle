from generate_json_solvers import GenerateJSONSolvers
from solver_generators.word_comparisons import WordComparison
from definitions import ROOT_DIR
from collections import defaultdict
from datetime import datetime
from itertools import product

import os
import json

from typing import List

OUTPUT_CONTENT = """
# Word Splits
## Explanation
One of the solvers looks at each word and determines the greatest number of
possible responses. For example, `stare` has more possible responses than
`sassy` for a few reasons:
1. `stare` is made of some of the most common letters. This means it overlaps
with a lot of words
2. `stare` has a greater variety of letters than `sassy` because `sassy` has
three s's
3. `sassy` has three of the same letter, so some responses are impossible. For
example, there's no way to get the response `YBYYB` saying that the three s's 
   appear in the answer but not in the correct positions.
    
Given all of these considerations, we wanted to know what the best and worst
words are in terms of splitting. Below are five from those extrema and the
full sorted list can be found in `word_splits.json`

## Top 5 Most Splits
Word | Splits | 0 Green | 1 Green | 2 Greens | 3 Greens | 4 Greens | 5 Greens
--- | --- | --- | --- | --- | --- | --- | ---
{best_rows}

## Top 5 Fewest Splits
Word | Splits | 0 Green | 1 Green | 2 Greens | 3 Greens | 4 Greens | 5 Greens
--- | --- | --- | --- | --- | --- | --- | ---
{worst_rows}

## Theoretical Bests
As mentioned above, a word that has unique letters (letter pattern `11111`) has
the most possible response patterns. Unsurprisingly, a word with all the same
letter (letter pattern `5`) has the fewest with only 6 possible responses.
Words like `fluff` (word pattern `311`), `ayaya` (word pattern `32`), and
`qajaq` (word pattern `221`) fall somewhere in between. This table goes through
the possible letter patterns and how many possible splits they have. This
shows that `ayaya` is punished by the word pattern present and not by the
letter choice.

Letter Pattern | Splits | 0 Green | 1 Green | 2 Greens | 3 Greens | 4 Greens | 5 Greens 
--- | --- | --- | --- | --- | --- | --- | ---
{theoretical_rows}
"""
ROW_TEMPLATE = "{word} | {total} | {split_data}"

class CalculateWordSplits(object):
    README_FILEPATH = "reports/report_output/word_splits.md"
    JSON_FILEPATH = "reports/report_output/word_splits.json"
    JSON_DETAILS_FILEPATH = "reports/report_output/word_splits_breakdown_{side}.json"

    def _get_top_n_words(self, split_count_words: dict, n: int, descending=True) -> List[str]:
        """
        Return the top N words
        """
        top_words = []
        for key, val in sorted(split_count_words.items(), reverse=descending):
            for word in val:
                top_words.append(word)
                if len(top_words) == n:
                    return top_words

    def _generate_full_word_split_breakdown(self, full_word_list: List[str]) -> dict:
        """
        Generate the full breakdown of word splits
        """
        json_output_full_path = os.path.join(ROOT_DIR, self.JSON_FILEPATH)
        if os.path.exists(json_output_full_path):
            with open(json_output_full_path, 'r') as f:
                json_output = json.load(f)
                split_count_words = {int(key): val for key, val in json_output.items()}
        else:
            split_count_words = defaultdict(list)

            # Loop over the words and store how much they split the options
            for index, guess in enumerate(full_word_list):
                split_count = len(WordComparison.split_into_pattern_match_groups(guess=guess, word_list=full_word_list))
                split_count_words[split_count].append(guess)

                if index % 100 == 0:
                    print("%s: Index %d out of %d" % (datetime.now(), index, len(full_word_list)))

            # Store the JSON information for the splits
            with open(json_output_full_path, 'w') as f:
                json_output = {"{:03d}".format(key): val for key, val in split_count_words.items()}
                json.dump(json_output, f, sort_keys=True, indent=2)

        return split_count_words

    def _get_table_row(self, word: str, green_split_data: dict) -> str:
        """
        Turns the input data into an output table row
        """
        # Get the green split data
        green_split_number_strs = []
        for count in range(5 + 1):
            green_split_number_strs.append(str(green_split_data.get(count, 0)))

        return ROW_TEMPLATE.format(
            word=word,
            total=sum(green_split_data.values()),
            split_data=" | ".join(green_split_number_strs)
        )

    def _get_theoretical_limits(self) -> str:
        """
        Generate the theoretical limits for each word pattern
        """
        word_patterns = [
            ('abcde', 11111),
            ('aabcd', 2111),
            ('aabbc', 221),
            ('aaabc', 311),
            ('aaabb', 32),
            ('aaaab', 41),
            ('aaaaa', 5)
        ]

        table_rows = []
        for word_pattern_str, word_pattern_int in word_patterns:
            # Generate the vocabulary we'll use for these tests
            vocabulary = set(char for char in word_pattern_str)
            vocabulary.add('x')

            # Store the unique patterns
            unique_patterns = set()
            for raw_word in product(vocabulary, repeat=5):
                answer = "".join(raw_word)
                unique_patterns.add(WordComparison.word_match(guess=word_pattern_str, answer=answer))

            # Get the green count
            correct_position_splits = defaultdict(int)
            for pattern in unique_patterns:
                correct_position_splits[pattern.count(WordComparison.MATCH_POSITION)] += 1

            table_rows.append(self._get_table_row(str(word_pattern_int), correct_position_splits))

        return "\n".join(table_rows)

    def run(self):
        """
        Loop over all the words and determine how many buckets each word splits the list into
        """
        full_word_list = GenerateJSONSolvers.load_word_list()

        split_count_words = self._generate_full_word_split_breakdown(full_word_list)


        # Get the top and bottom 5
        extremes = {
            'top': self._get_top_n_words(split_count_words, 5, True),
            'bottom': self._get_top_n_words(split_count_words, 5, False)
        }
        output_rows = {
            'top': [],
            'bottom': []
        }
        for side, guesses in extremes.items():
            guesses_data = {}
            for guess in guesses:
                split_data = WordComparison.split_into_pattern_match_groups(guess=guess, word_list=full_word_list)

                # Convert each split into a count and example
                guess_data = {}
                correct_position_splits = defaultdict(int)
                for pattern, words in sorted(split_data.items()):
                    guess_data[pattern] = {
                        'words': len(words),
                        'example': words[0]
                    }
                    correct_position_splits[pattern.count(WordComparison.MATCH_POSITION)] += 1
                guesses_data[guess] = guess_data
                output_rows[side].append(self._get_table_row(guess, correct_position_splits))

            # Save the data
            with open(os.path.join(ROOT_DIR, self.JSON_DETAILS_FILEPATH.format(side=side)), 'w') as f:
                json.dump(guesses_data, f, sort_keys=True, indent=2)


        # Save the documentation
        output = OUTPUT_CONTENT.format(
            best_rows="\n".join(output_rows['top']),
            worst_rows="\n".join(output_rows['bottom']),
            theoretical_rows=self._get_theoretical_limits()
        )
        with open(os.path.join(ROOT_DIR, self.README_FILEPATH), 'w') as f:
            f.write(output)

if __name__ == '__main__':
    CalculateWordSplits().run()
