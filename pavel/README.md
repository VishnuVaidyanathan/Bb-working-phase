# Pavel Kropitz's earlier BB(7) champion, read as words (21 Nov 2026)

Machine `1RB0RA_1LC1LF_1RD0LB_1RA1LE_1RZ0LC_1RG1LD_0RG0RF` found by Pavel Kropitz (bound 2 ^(11) 2 ^(11) 3 on the bbchallenge wiki).
`look.py` prints the tape as runs; `words.py` reads it as words (a run of 1s with the 0s after it, written ones.zeros).

Observed on the real run from a blank tape (tape read each time state A reaches a fresh cell at the right end):
* The tape is a list of counters. A counter is a run of the word `10` (written 1.1); counters are separated by the word `110` (2.1);
  the list ends with `100 111` (1.2 3.3).  Example at step 20,236:
  `3.1 (1.1)x3 2.1 (1.1)x3 2.1 ... (1.1)x33 2.1 (1.1)x13 2.1 (1.1)x56 1.2 3.3`  = counters 3, 3, ..., 33, 13, 56.
* Work happens at the right end: the last two counters (a, b) become (a-1, b+2), again and again, until a is used up.
  (seen: 14,54 -> 13,56 -> 12,58 ...)
* At step 932 a single counter of 13 (then written as 13 words `100`) is turned into a row of 13 small counters.
  13 - 2 = 11, the number of arrows in the published bound.  So "arrows = stores in the row - 2" fits this machine as well.
So his grammar is also a row of stores worked level by level, with the multiplier 2 and the work at the right end; the coding is
different (words of 2 and 3 cells instead of blocks and gaps).  Status: observed. Rules not yet written as arithmetic or checked.

## Second reading: the list of counters (counters.py; observed, 30 million steps, 5,193 visits)

* 5,091 of the visits (98%) have the right end `... 2.1 a 2.1 b 1.2 3.3` and differ from the visit before by the plain transfer
  (a, b) -> (a-1, b+2).  So a counter a is emptied into the last one: b + 2a.
* The other 112 steps are the turns between transfers. They pass through in-between shapes (`3.1`, `1.2 3.2 ... 1.3`, `n 3.3`).
  Read across them: when a is used up, with a counter c to its left,
      (c, 0, b)  ->  (c-1, b+6, 2)      seen: (3, 0, 10) -> (.., 16, 2);  (.., 0, 34) -> (.., 40, 2)
  and the transfers then give 2 + 2(b+6) = 2b + 14.   Seen: 10 -> 34 -> 82.
  So one unit of c doubles the last counter (2b+14); c is the payer and pays 1.
* An empty counter is two markers side by side (`2.1 2.1`), so a list like `2.1 2.1 2.1 2.1 2.1 2.1 2.1 1 3.3` is seven empty counters and a 1.
* The row: at step 932 thirteen words `100` stand in a row; they are turned into counters one at a time (first a 6, then 3s).
In our stack terms: block at the right end, round "x2", fresh stores of 3, payer pays 1, old block +6 becomes the store.
Not done: the rules for two or more empty counters, the row rule, where the halt (state E reading 0) is met, and a check at every visit.

## Rules as arithmetic, checked (rules.py thought experiments, model.py against the real run)

Canonical visit: lead word, counters, last counter b at the right end.
* transfer: the counter a next to the last is not empty -> a-1, b+2
* ticket: g empty counters before the last, payer c >= 3 before them -> payer c-3; then b+7 (g = 1), or b+5, g-2 counters of 3,
  a counter of 5 (g >= 2); then a new last counter 0
* payer of 1 -> HALT; payer of 2 with something to its left -> HALT; payer of 2 at the left end -> the lead word grows (row event)
model.py: 5,112 canonical visits of the real run (30 million steps) agree, 0 differ; 2 are row events at the left end, not modelled.
The builder reproduces 360 of 360 real steps.

So his gate is in THREES: a payer pays 3 at a time and the machine halts when a payer has 1 left. His multiplier is 2.
Jeff Ketchersid's gate is in twos with multiplier 3. In both, the multiplier and the gate number share no divisor.
Pavel's machine is "round x2, payers of 3" - the combination our own gate study found to fire (our loose version needs 8 states).

Start states (blank tape): only A gives the stack (row of 13). C halts at step 860, E at once; B, D, F, G do not build anything.

## The lead word is a clock in fours (thought experiments, 21 Nov)

A lone counter of 4 with a lead word of k ones:
k = 1: row of 12;  k = 2: the counter becomes 7, then a row of 16;  k = 3: row of 13 (this is his real run);  k = 4: HALT at once;
k = 5: halts after a few hundred steps;  k = 6: goes on without a row;  k = 7: row of 17;  k = 8: HALT.
So the machine reads the lead word in fours: a row at 3 (and 7), the halt at 4 (and 8). Each time the list is used up the lead grows by 1.
His blank-tape boot arrives at lead 3 with a counter of 4: one row of 13, then lead 4, halt. That is his 11 arrows.
A boot that arrived one step earlier on the clock with the same engine would make a second row from a tower-sized counter.
His table from a blank tape cannot: all seven start states were tried.

## Lead word and lone counter together (leadmap.py, thought experiments, 21 Nov)

Start: a lead word of k ones and one lone counter c (c = 1..9). Tested on the real table:
- k = 1, 2 or 3: the lead word first grows to 3, then one row is made. Row length (first list of 8+ counters seen):
  k = 1: 2c+5,   k = 2: 2c+9,   k = 3: 2c+6.   (leadmap counts one more than pavel/model does: his own run, k = 3 and c = 4, shows as 14 here.)
- k = 4: halts at once, for every c.
So the engine is "one row, then the lead word reaches 4 and it halts". The size of the machine is set by one number: the lone counter
at the moment the lead word is 3.  His boot gives 4.  The same engine with a lone counter of 9 or more would have a first row past
Jeff Ketchersid's 22.  Not checked here: whether a payer runs out (payer of 1 or 2) inside such a longer row, which would halt it early.
