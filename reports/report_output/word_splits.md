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


## Top 5 Fewest Splits
