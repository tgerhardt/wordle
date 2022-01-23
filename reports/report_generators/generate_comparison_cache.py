from generate_json_solvers import GenerateJSONSolvers
from solver_generators.word_comparisons import WordComparison
from definitions import ROOT_DIR

import gzip
import json
from datetime import datetime
import os
from collections import defaultdict

OUTPUT_CONTENT = """{rows}"""
TIME_ROW = """{use_cache} | {time_delta}"""

class GenerateComparisonCache(object):
    OUTPUT_FILEPATH = "reports/report_output/comparison_cache_speedup.md"

    def run(self):
        """
        Loop over all the pairs of words and get the info for when its cached
        """
        # Load the word list
        full_word_list = GenerateJSONSolvers.load_word_list()

        cache_data = defaultdict(dict)
        output_rows = []
        for use_cache in [False, True]:
            # Start the timer
            start_datetime = datetime.now()
            print("Starting 'use_cache: %s' run: %s" % (use_cache, start_datetime))
            wc = WordComparison(use_cache)

            # Loop over the words
            for index, guess in enumerate(full_word_list[:1000]):
                for answer in full_word_list:
                    result = wc.word_match(guess=guess, answer=answer)
                    if use_cache is False:
                        if result != wc.MISS:
                            cache_data[guess][answer] = result

                if index % 100 == 0:
                    print("%s: Index %d out of %d" % (datetime.now(), index, len(full_word_list)))

            end_datetime = datetime.now()
            print("Completed 'use_cache: %s' run: %s" % (use_cache, end_datetime))
            output_rows.append(TIME_ROW.format(use_cache=use_cache, time_delta=str(end_datetime - start_datetime)))

            # Save the file
            if use_cache is False:
                with gzip.open(os.path.join(ROOT_DIR, wc.MATCH_CACHE_FILENAME), 'wb') as f:
                    f.write(json.dumps(cache_data).encode('utf-8'))


        # Save the result
        output = OUTPUT_CONTENT.format(rows="\n".join(output_rows))
        with open(os.path.join(ROOT_DIR, self.OUTPUT_FILEPATH), 'w') as f:
            f.write(output)

if __name__ == '__main__':
    GenerateComparisonCache().run()
