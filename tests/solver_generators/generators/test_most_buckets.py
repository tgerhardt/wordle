import unittest

from solver_generators.generators.alphabetical import AlphabeticalGenerator


class TestAlphabeticalGenerator(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None  # Let us see the totality of the problem

    def test_generate_solver(self):
        """
        Check that we generate a sensible solver
        """
        word_list = ['APPLE', 'BEETS', 'CARDS', 'DRIVE', 'HELLO', 'ITEMS', 'JUMPS', 'LIONS',
                     'PEARS', 'QUIET', 'SMITE', 'TANGY', 'WORLD']

        expected_output = {
            'guess': 'APPLE',
            'branches': {
                'BBBBG': {
                    'guess': 'DRIVE',
                    'branches': {
                        'BBGBG': {'branches': {}, 'guess': 'SMITE'}
                    }
                },
                'BBBBY': {
                    'guess': 'BEETS',
                    'branches': {
                        'BBGYG': {'branches': {}, 'guess': 'ITEMS'},
                        'BYBYB': {'branches': {}, 'guess': 'QUIET'}
                    },
                },
                'BBBGB': {'branches': {}, 'guess': 'WORLD'},
                'BBBGY': {'branches': {}, 'guess': 'HELLO'},
                'BBBYB': {'branches': {}, 'guess': 'LIONS'},
                'BYBBB': {'branches': {}, 'guess': 'JUMPS'},
                'YBBBB': {
                    'guess': 'CARDS',
                    'branches': {
                        'BGBBB': {'branches': {}, 'guess': 'TANGY'}
                    },
                },
                'YYBBY': {'branches': {}, 'guess': 'PEARS'}},
        }

        generator = AlphabeticalGenerator(AlphabeticalGenerator.MODE_HARD, word_list)
        self.assertDictEqual(expected_output, generator.generate_solver())


if __name__ == '__main__':
    unittest.main()
