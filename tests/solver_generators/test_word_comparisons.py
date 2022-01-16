import unittest
from collections import namedtuple

from solver_generators.word_comparisons import WordComparison

TEST_CASE_CLASS = namedtuple('TestCase', ('args', 'expected_output'))

class TestWordComparison(unittest.TestCase):
    def test_word_match(self):
        """
        Check that word matching works
        """
        test_cases = [
            TEST_CASE_CLASS(('CAGED', 'LIONS'), 'BBBBB'),  # No overlap
            TEST_CASE_CLASS(('START', 'HEART'), 'BBGGG'),  # Three correct positions
            TEST_CASE_CLASS(('ITEMS', 'SMITE'), 'YYYYY'),  # Anagram
            TEST_CASE_CLASS(('ADDED', 'CADDY'), 'YYGBB'),  # Repeated letters with some overlap
            TEST_CASE_CLASS(('ADDED', 'DATED'), 'YYBGG')  # Repeated letters with some overlap
        ]
        for test_case in test_cases:
            self.assertEqual(test_case.expected_output, WordComparison.word_match(*test_case.args))

    def test_split_into_pattern_match_groups(self):
        """
        Check that we correctly split words into groups
        """
        expected_output = {
            'GGGGG': ['SMITE'],
            'GGBGG': ['SMOTE'],
            'GBGBG': ['SPIRE'],
            'BYYYY': ['TIMER'],
            'BBBBB': ['CADDY'],
            'YYYYY': ['TIMES', 'ITEMS']
        }
        output = WordComparison.split_into_pattern_match_groups(
            "SMITE", ["SMITE", "SMOTE", "SPIRE", "TIMER", "CADDY", "TIMES", "ITEMS"]
        )

        self.assertDictEqual(expected_output, output)

if __name__ == '__main__':
    unittest.main()
