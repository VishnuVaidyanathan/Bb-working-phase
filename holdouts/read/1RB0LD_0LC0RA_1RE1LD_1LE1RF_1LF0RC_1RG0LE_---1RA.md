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

## Correction and a second reading (22 Nov): prurq's analysis (Discord Busy Beaver community), shared by Vishnu

prurq calls this machine TM 721 and reads it at configs `0^inf 1^(2n+1) G> (10)^i (1011)^1`.  Their findings (theirs, not ours):
every `1110` block is used up by one per LEVEL, and the levels are arrows: `0^inf 1^(2n+1) G> (10)^(i+1) (11)^k` goes like 2 ^(i arrows) k.
The next "overflow" (the counter turning into a new run of `1110` blocks) comes after about 2^65538 arrows; they followed it as far as
`1^25 G> 10101011 (1011)^(2^65538-6) 11`.  They think it does not halt: the halt seems to depend on X and Y in twos at
`0^inf 1^X G> (10)^Y 0^inf`, and the rules seem to keep both the same in twos (their conjecture, not analysed further).  They add that
this is surely not the only machine in the list with this arrow mechanism, and that some may halt after several overflows.
What this corrects in our reading above:
* I wrote "one more exponential per store".  Wrong: one more ARROW per store.  I had only followed the first two levels.
* I wrote that Quick_Sim cannot hold the row.  Wrong as stated: with a block size of 4 (`-n 4`) our copy does not run out of memory
  (it reached 10^429,162 in 100 s); prurq's runs reach level-10 rules.  It died for us because the block finder chose blocks of 2.
What agrees: rows of rows ("overflow" = our "lone counter becomes a row"); 2^65,53x at the first overflow; and their mod-2 remark is
our gate rule - multiplier 2 with payments of 2 keeps everything the same in twos, so no number test.
