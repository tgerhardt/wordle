"""
Find the word that will get the most upcoming words in only two guesses
"""
from datetime import date, datetime
from solver_generators.word_comparisons import WordComparison
from generate_json_solvers import GenerateJSONSolvers
import json
import os
from definitions import ROOT_DIR

from typing import List

class CheatingWordFinder(object):
    START_DATE_INCLUSIVE = date(2022, 1, 23)

    # Map the answers to dates
    REFERENCE_ANSWER = 'crimp'
    REFERENCE_DATE = date(2022, 1, 22)

    CHEAT_OUTPUT_FILENAME = 'reports/report_output/cheating_word.json'

    def _get_answers_from_start_date(self) -> List[str]:
        """
        Return the list of answers starting with the start date
        """
        answers_list = GenerateJSONSolvers.load_answer_list()
        reference_index = answers_list.index(self.REFERENCE_ANSWER)
        days_delta = (self.START_DATE_INCLUSIVE - self.REFERENCE_DATE).days
        return answers_list[reference_index + days_delta:]

    def run(self):
        """
        Loop over all the words. Find the word that gives the highest number of unique patterns for the longest time
        """
        future_answers = self._get_answers_from_start_date()
        full_word_list = GenerateJSONSolvers.load_word_list()

        # Find the best word
        best_word = None
        best_streak = 0
        for index, guess in enumerate(full_word_list):
            patterns = set()
            for answer in future_answers:
                pattern = WordComparison.word_match(guess=guess, answer=answer)
                if pattern not in patterns:
                    patterns.add(pattern)
                else:
                    # Hit the limit
                    if best_streak < len(patterns):
                        best_streak = len(patterns)
                        best_word = guess

                    # Move to the next guess
                    break

            if index % 1000 == 0:
                print("%s: Index %d out of %d. Best word so far '%s': %d" % (
                    datetime.now(), index, len(full_word_list), best_word, best_streak
                ))

        # Output the decision tree from it
        raw_decision_tree = WordComparison.split_into_pattern_match_groups(best_word, future_answers[:best_streak])
        best_answer_info = {
            'guess': best_word,
            'streak_length': best_streak,
            'streak_start': str(self.START_DATE_INCLUSIVE),
            'decision_tree': {pattern: val[0] for pattern, val in raw_decision_tree.items()}
        }
        # Save the data
        with open(os.path.join(ROOT_DIR, self.CHEAT_OUTPUT_FILENAME), 'w') as f:
            json.dump(best_answer_info, f, sort_keys=True, indent=2)


if __name__ == '__main__':
    CheatingWordFinder().run()
