import unittest

from solver_generators.generators.most_buckets import MaxBucketsGenerator
from tests.solver_generators.generators.common_test_cases import BaseTestGeneratorWrapper

class TestMaxBucketsGenerator(BaseTestGeneratorWrapper.BaseTestGenerator):
    GENERATOR_CLASS = MaxBucketsGenerator

    FIND_GUESS_EASY_FLOWN = 'flown'

if __name__ == '__main__':
    unittest.main()
