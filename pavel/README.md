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
