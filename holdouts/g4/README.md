# A holdout with a gate and a tower, read by hand (21 Nov)

`1RB0LG_1RC0RA_1LD1LE_1LB0LC_0LF0RE_0LG0LC_0RA---`  (from Polygon's holdout list; halts on 17 of 200 small test tapes)

Tape as a list (tok.py): a number n = n words `10`; `|` = `100`; `#` = `1000`. Visits in state E at the right end. Observed from a blank tape:

    1 | | #  ->  1 # 2 #  ->  | 3 | #  ->  | | 6 #  ->  # 8 #  ->  9 | #  ->  ...  ->  | 18 #  ->  20 #
    20 #     ->  1 | | | ... | #      (a row of 21 bars, step 3,879)
    then the row is worked from the right, one bar at a time:   k | n | #  ->  k | | 2n #  ->  k # 2n+2 #  ->  k-1 | 2n+3 | #

So it is a doubling stack like the others: a lone counter M becomes a row of M+1 stores. Its first row (21) is longer than Pavel Kropitz's (13).

The gate (small_lists.py, tested): of all lists up to 6 tokens with counters up to 5, the machine halts on exactly those that end in `# #`
(626 lists, all halt in 27 steps; none of any other form halts).
The rules above never write `# #` at the end: the nearest step is `| | n #  ->  # n+2 #`, and n+2 is never 0.
So the halting wire is there, but no number is tested on the way to it. Observed, not proved: this machine most likely never halts.

## It makes row after row (rows.py, observed)

Started on a lone counter of 1:  row of 2 bars (step 86)  ->  lone counter 20 (step 1,188)  ->  row of 21 bars (step 3,858)  ->  ...
So a finished row hands its result to the next row.  The blank-tape run is this same sequence.  The engine "towers over towers" exists in 7 states;
what this table lacks is only a halt.
