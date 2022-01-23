# Comparison Cache Speedup
## Explanation
Most of the solvers compare every possible guess against every possible answer.
This is an `O(g*a)` operation and there's not a lot of ways to speed it up.
(One idea is to bucket the words to determine which ones share letters and
which don't but it's not easy to do.) The easiest speedup is to cache if two
words overlap. 

## 1K Words Runtime
To get an idea of how long it takes to run, we cache the results for the first
1K guesses versus all answers. As shown in the table below, the speed up is
8.4x. Based on this runtime, we expect it would take 31m to run through all
guesses without caching and 4m with caching, saving 27m.

| Use Case | Runtime |
| --- | --- |
| False | 0:02:23.536030 |
| True | 0:00:17.006485 |

## Limitations
Unfortunately, we ran into a MemoryError at around 3-4K guesses. We're only
storing the matches to try to save space. Reducing the number of guesses to
3K still ran into MemoryErrors during the cached run. Given this, it appears
that memory isn't being properly cleaned up. We'll have to use this limitation
when trying to cache results in the future. A smart partial cache system
may also be possible. For example, even caching 1K words saved about two
minutes. A partial cache like this could still speed things up.