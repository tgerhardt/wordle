import json
import os

from solver_generators.base_generator import BaseGenerator
from solver_generators.generators.alphabetical import AlphabeticalGenerator
from solver_generators.generators.information import InformationGenerator
from solver_generators.generators.most_buckets import MaxBucketsGenerator
from solver_generators.generators.smallest_bucket import SmallestBucketGenerator
from definitions import ROOT_DIR

class GenerateJSONSolvers(object):
    SOLVER_GENERATORS = {
        'alphabetical': AlphabeticalGenerator,
        'information': InformationGenerator,
        'max_buckets': MaxBucketsGenerator,
        'smallest_bucket': SmallestBucketGenerator
    }
    MODES = [
        BaseGenerator.MODE_HARD,
        BaseGenerator.MODE_EASY  # Doesn't work yet
    ]

    WORD_LIST_FILEPATH = 'solver_generators/static_files/fiveletterwords.txt'
    GENERATOR_OUTPUT_FILEPATH_TEMPLATE = 'solvers/json/{mode}/{solver}.json'

    def __init__(self):
        """
        Load the word list
        """
        self._full_word_list = []
        with open(os.path.join(ROOT_DIR, self.WORD_LIST_FILEPATH), 'r') as f:
            for line in f.readlines():
                self._full_word_list.append(line.strip())

    def run(self):
        """
        Generate the JSON solvers if they don't already exist
        """
        for mode in self.MODES:
            for name, generator in self.SOLVER_GENERATORS.items():
                saved_solver = self.GENERATOR_OUTPUT_FILEPATH_TEMPLATE.format(mode=mode, solver=name)
                print('Generating Solver "{solver}", Mode "{mode}"'.format(mode=mode, solver=name))

                if os.path.exists(saved_solver):
                    print('Already Generated')
                else:
                    output = generator(mode, self._full_word_list).generate_solver()
                    with open(os.path.join(ROOT_DIR, saved_solver), 'w') as f:
                        json.dump(output, f, sort_keys=True, indent=2)
                    print('Generation Complete')


if __name__ == '__main__':
    GenerateJSONSolvers().run()
