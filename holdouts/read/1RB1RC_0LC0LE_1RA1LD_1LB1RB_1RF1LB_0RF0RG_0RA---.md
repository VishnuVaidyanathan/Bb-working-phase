# `1RB1RC_0LC0LE_1RA1LD_1LB1RB_1RF1LB_0RF0RG_0RA---` read in full (22 Nov) - the one arrow machine in Polygon's list that triples

Words: a counter n = n words `10`;  | = `100`;  # = `1000`;  % = `10000`.  Lists read at the far-left turns in state E
(holdouts/leftlists.py; observed on the real run, not proved):

    1  ->  | | 1  ->  | 3 |  ->  5 |  ->  8                              start
    8  ->  | | | | | | | | | 1                                           OVERFLOW: a lone counter n becomes a row of n+1 bars
    | | | ...      ->  | 3 # ...     ->  5 # ...                         three bars open a level: a fresh counter and a marker
    5 # | ...      ->  | | 5 # ...   ->  | 3 | 4 # ...  ->  5 | 4 # ...  one bar is taken from the row
    5 | 4  ->  8 | 3  ->  11 | 2  ->  14 | 1  ->  17 |                   ROUND: the second counter pays 1, the first gains 3
    17 | # ...     ->  | 18 % ...    ->  20 % ...                        the second counter is empty: | and # join into %
    20 % | ...     ->  | | | 19 # ... ->  5 # 19 # ...                   a bar is taken; % becomes #; the 20 pays 1 and stays as a deeper counter
    5 # 19 #       ->  | | 5 | 18 #  ->  ... 17 | | 18 #  ->  20 # 18 #  the 19 pays 1; rounds; ...
    20 # 18 #      ->  | | 20 | 17 # ->  | 3 | 19 | 17 #                 the block (20) LANDS as the middle counter, a new block starts
    ... 5 | 19 | 17 -> 8 | 18 | 17 -> ... 35 | 9 | 17 ...                rounds again: +3 per unit

How it works, in our words:
* round: pay 1, gain 3 (so the block is about 3 times the counter it used up);
* landing: when a counter is used up, the next one pays 1 and the block lands in its place, at whatever depth;
* the depth is carried by the WIDTH OF THE MARKER: | , # , % have 2, 3, 4 empty cells.  An empty level is one more empty cell in the
  marker (| and # join into %); taking a bar from the row makes the marker one cell narrower and puts fresh bars in front.
  The count of empty levels is never held in a state: it sits on the tape as the width of one gap.
* levels = bars of the row, one arrow per bar; overflow: lone counter n -> n+1 bars.
Every payment is by 1.  Nothing is paid in twos or threes.  (Correction: earlier today I wrote that its rows are "cut in twos" and
that it meets the gate rule.  Wrong: I had counted cells; the 17 cells were a counter of 8 words.  In words it is n -> n+1 bars.)
Halt wire: G reading 1; G is entered only from F1 (`0RG`), and F from E0 (`1RF`) or F0.  So the halt needs two 1s side by side just
right of a cell E has written - a `11`, which its words (`10`, `100`, `1000`, `10000`) never contain.  A shape, not a number.
So it is g4's grammar with gain 3 in place of gain 2: a tripling stack with zero tests only.  No number test seen.
Quick_Sim (100 s): no halt, level 6, about (10^^^^^)^31 and climbing.  Whether it halts: not known; we see no reason for it to.
