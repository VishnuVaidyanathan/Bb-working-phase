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
