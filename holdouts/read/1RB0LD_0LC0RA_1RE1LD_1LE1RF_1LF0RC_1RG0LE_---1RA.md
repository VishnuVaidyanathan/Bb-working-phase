# `1RB0LD_0LC0RA_1RE1LD_1LE1RF_1LF0RC_1RG0LE_---1RA` read by hand (22 Nov, at Vishnu's request)

It is in Polygon's list of BB(7) holdouts.  Our earlier code for it was U2 ("has a halting gate, small growth") - the "small growth"
part was WRONG: Shawn Ligocki's Quick_Sim does not grow slowly on it, it runs out of memory (see below).

Layout: runs of 1s with ONE empty cell between them.  Read at the far-left blank cell in state D (tested, direct run):
    step        149:  3 3 3 4
                281:  3 11 1 4
                949:  3 3 27 2
               1669:  3 27 23 2
               4129:  3 59 21 2      ... 123 19, 251 17, 507 15, 1019 13, 2043 11, 4091 9 ...
         55,900,357:  3 8187 7 2
Rules seen (observed, not proved):
* inside: the second counter b pays 2, the first gains 4, until b is 1; then they join: b -> 2b + 5  (11, 27, 59, 123, 251 ...).
* each such doubling costs the third counter c 2  (27, 25, 23 ...).  When c is down to 1, the last number r pays 2 and c is refilled
  from the big b.  r went 4 -> 2; it has one payment left.
* hand-made tapes with nothing behind: (3 3 3) -> 3 11 1 -> 3 28 -> lone 59 -> a ROW: 61 stores of 3 and a 4.
  (3 3 5) -> lone 123 -> 125 stores of 3 and a 4.   So a lone counter M becomes a row of M+2 stores of 3 with a tail of 4.
* the row is then worked from the left: 3 11 1 (3)^58 4 -> (3)^2 27 1 (3)^57 4 -> 3 11 25 1 (3)^57 4 -> ...  each store of 3 that is
  taken refills c from b, i.e. one more exponential per store.
So it has rows of rows: counter -> row as long as the counter -> counter ...  Multiplier 2, payments of 2, all counters odd.
Real run: direct, 2,000,000,000 steps, no halt, 53,798 ones, 5 runs, longest 42,054.  By the rules c reaches 1 near step 3.6 billion
with b about 65,531; then b doubles about 65,000 times and the lone counter (about 10^19,728) becomes a row that long.
Quick_Sim (run through calc/quick_sim_with_remainders.py, 110 s): reaches "Num Nonzeros 10^19,728 .. 10^19,731" with the tape
written out as `10 11 10 11 ...` and is then killed for memory.  It cannot hold a row that long.
Halt wire: G reading 0, entered only from F0 (`1RG`): it needs two empty cells in a row where F writes.  With multiplier 2 and
payments of 2 the counters stay odd, so we see no number test (gate rule).  Whether it ever halts: not known.
Same kind as holdout g4 (rows of rows, no number test seen), but a different engine: solid counters, not `10` words.
