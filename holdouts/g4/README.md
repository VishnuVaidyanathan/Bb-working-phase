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

## Where the halt wire looks (by hand, 21 Nov night)

Halt = G reading 1.  G is entered from A1 and from F0 (both `0LG`).  Counted over 3,000,000 steps from a blank tape: 23 different local
shapes, G always reads 0.
* From A1 - can never halt (local argument, proved for this table): A is entered only moving right (from G0 or B1, both write 0 behind them),
  so when A1 steps back left, G reads the 0 just written.
* From F0 - the only way to the halt.  The chain is C1 (C on a 1, steps left), E0, F0, G.  So C, standing on the first cell of a word,
  looks at what is on its left:
      one zero then a 1 (a `10` word)        -> F1: carry on to the left
      exactly two zeros then a 1 (a bar)     -> G reads 1: HALT
      three or more zeros (a `#` or blank)   -> G0, A0, B0: fill and go on
  So the halt asks: "is the word on my left a bar?".  It is a three-way look that the engine already uses for its work.

Rules of the row work, read from the lists (observed):   k # n #  ->  k-1 | n+1 | #  ->  k-1 | | 2n+2 #  ->  k-1 # 2n+4 #
k counts down by 1 while n goes n -> 2n+4.  When k is used up, two more bars are taken from the row and the old n becomes the new k.
When the bars are used up the lone counter M makes a new row of M+1 bars.
Two things count down (k inside a row, the bars of the row).  Nothing counts down at the level of rows: every lone counter makes a row.
What g4 lacks is that third count.  By Vishnu's note it does not need the halt wire: it only has to leave a bar where C looks.

## The step "lone counter M -> row of M+1 bars", traced cell by cell (lone.py, 21 Nov night)

M = 1..9 (tested): always `1 | ... | #` with M+1 bars; steps 86, 132, 188, 254, 330, 416, 512, 618, 734; the left edge moves M+3 cells.
How (trace of M = 3): one walk per word.  Each walk goes to the left end (D1, C0 shift the `10` words), turns (D0, B0, C1, E1), comes
back with an 8-wire shuttle (A0 B0 C1 E1 E1 E0 F0 G0) and turns the right-most `10` left into `110`.  When no `10` is left, D reads 0
instead of 1 (the only test), and one last sweep turns every `110` into a bar.
So this step takes the words ONE at a time and tests only "none left".  M is never tested in twos or threes.

Numbers (from the row rules): n -> 2n+4, and the lone counter is M = 2n+2, so M is always even.  A test in twos would always see the same
answer; only a test in threes (or a multiplier of 3 with a test in twos) can see a different answer from row to row (gate rule: the stride
of the test and the multiplier must share no divisor).  g4 doubles, counts down by ones, and has no wire left: it has no number test at
any of its three levels.  Observed and traced, not proved.
