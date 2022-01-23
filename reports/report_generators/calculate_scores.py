from generate_json_solvers import GenerateJSONSolvers
from solver_generators.base_generator import BaseGenerator
from definitions import ROOT_DIR

from typing import List

import os
import json

OUTPUT_CONTENT = """
# Solver Scores
## Explanation
The solvers are stored in JSON files under solvers/json/. These files contain
all the guesses the solver will do depending on the matches thus far. This
file is generated by `generate_json_solvers.py` to score each solver. These
scores can be used to compare solvers and see improvements as we write new
ones.

## Scores
| Solver | Mode | 1 Guess | 2 Guesses | 3 Guesses | 4 Guesses | 5 Guesses | 6 Guesses | Remaining | Percentage 6 Guesses or Fewer |
|--------|------|---------|-----------|-----------|-----------|-----------|-----------|-----------|-------------------------------|
{rows}
"""
SOLVER_ROW_TEMPLATE = "{solver} | {mode} | {counts} | {percentage}"

class CalculateSolverScores(object):
    OUTPUT_FILEPATH = "reports/report_output/solver_scores.md"

    def _recursively_count_words(self, sub_solver: dict, depth: int) -> List[int]:
        """
        Recursively inspect the solver and return the number of words per depth
        """
        word_counts = [0] * (BaseGenerator.MAX_DEPTH + 1)
        word_counts[min(depth, BaseGenerator.MAX_DEPTH)] += 1  # This level

        if isinstance(sub_solver, list):
            # Don't recurse, just count
            word_counts[min(depth + 1, BaseGenerator.MAX_DEPTH)] += len(sub_solver)
        else:
            # Recurse on each branch
            for sub_sub_solver in sub_solver["branches"].values():
                sub_word_counts = self._recursively_count_words(sub_sub_solver, depth + 1)
                for index, val in enumerate(sub_word_counts):
                    word_counts[index] += val

        return word_counts


    def run(self):
        """
        Generate the JSON solvers if they don't already exist
        """
        solver_rows = []

        for mode in GenerateJSONSolvers.MODES:
            for name, generator in GenerateJSONSolvers.SOLVER_GENERATORS.items():
                saved_solver = GenerateJSONSolvers.GENERATOR_OUTPUT_FILEPATH_TEMPLATE.format(mode=mode, solver=name)
                print('Scoring Solver "{solver}", Mode "{mode}"'.format(mode=mode, solver=name))

                if os.path.exists(os.path.join(ROOT_DIR, saved_solver)):
                    # Load the data
                    with open(os.path.join(ROOT_DIR, saved_solver), 'r') as f:
                        solver_data = json.load(f)

                    word_counts = self._recursively_count_words(solver_data, 0)
                    counts_str = " | ".join([str(count) for count in word_counts])
                    percentage = 100.0 * (sum(word_counts[:-1]) / sum(word_counts))
                    row = SOLVER_ROW_TEMPLATE.format(solver=name, mode=mode, counts=counts_str,
                                                     percentage=("%.2f%%" % percentage))
                    solver_rows.append(row)

        # Save the result
        output = OUTPUT_CONTENT.format(rows="\n".join(solver_rows))
        with open(os.path.join(ROOT_DIR, self.OUTPUT_FILEPATH), 'w') as f:
            f.write(output)

if __name__ == '__main__':
    CalculateSolverScores().run()
