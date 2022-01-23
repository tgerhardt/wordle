
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
tares | 212 | 32 | 78 | 66 | 30 | 5 | 1
teras | 209 | 32 | 80 | 66 | 26 | 4 | 1
tears | 204 | 32 | 78 | 64 | 24 | 5 | 1
pelas | 202 | 32 | 75 | 64 | 25 | 5 | 1
pares | 201 | 32 | 76 | 61 | 26 | 5 | 1

## Top 5 Fewest Splits
Word | Splits | 0 Green | 1 Green | 2 Greens | 3 Greens | 4 Greens | 5 Greens
--- | --- | --- | --- | --- | --- | --- | ---
qajaq | 36 | 8 | 16 | 8 | 3 | 0 | 1
pzazz | 43 | 10 | 18 | 11 | 3 | 0 | 1
urubu | 49 | 12 | 22 | 12 | 2 | 0 | 1
ayaya | 50 | 8 | 19 | 15 | 6 | 1 | 1
jujus | 50 | 9 | 20 | 13 | 6 | 1 | 1

## Theoretical Bests
As mentioned above, a word that has unique letters (letter pattern `11111`) has
the most possible response patterns. Unsurprisingly, a word with all the same
letter (letter pattern `5`) has the fewest with only 32 possible responses.
Words like `fluff` (word pattern `311`), `ayaya` (word pattern `32`), and
`qajaq` (word pattern `221`) fall somewhere in between. This table goes through
the possible letter patterns and how many possible splits they have. This
shows that `ayaya` is punished by the word pattern and can only get less than
half the possible splits if the letters were unique.

Letter Pattern | Splits | 0 Green | 1 Green | 2 Greens | 3 Greens | 4 Greens | 5 Greens 
--- | --- | --- | --- | --- | --- | --- | ---
11111 | 238 | 32 | 80 | 80 | 40 | 5 | 1
2111 | 203 | 24 | 68 | 68 | 37 | 5 | 1
221 | 171 | 18 | 57 | 56 | 34 | 5 | 1
311 | 142 | 12 | 44 | 49 | 31 | 5 | 1
32 | 115 | 9 | 35 | 37 | 28 | 5 | 1
41 | 77 | 4 | 17 | 28 | 22 | 5 | 1
5 | 32 | 1 | 5 | 10 | 10 | 5 | 1
