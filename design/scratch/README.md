# A machine formed from scratch, from the words (22 Nov) - Vishnu's direction: do not edit, do not take a mechanism, form it

Words used: round (pay 2, gain 3 - a multiplier of 3/2 against a test in twos), look, land the block as the payer, a count carried
by one trip per level, start from a blank tape.  Layout: solid runs of 1s, one empty cell between them, the growing block on the left.

Each state was given its job first; the wires follow from the job:
    A  runner to the right        A1 `1RA` run over the block          A0 `1RB` fill the gap
    B  look at the payer          B1 `1RC` step over its first cell    B0 `1RE` payer empty: fill, look one level deeper
    C  pay / test                 C1 `0LD` erase the second cell       C0  HALT: the payer had exactly one cell left
    D  runner back to the left    D1 `1LD`                             D0 `1RA` write a cell at the left end, turn
    E  deep payer                 E1 `0LF` the deep store pays 1       E0 `0LF` that level is empty too: a free trip
    F  runner left after a deep event   F1 `1LF`                       F0 `0LG` leave an empty cell: the old block is now a store
    G  new block                  G0 `1RA` start it                    G1 `0LG` move the start one cell further (one per empty level)
Table: `1RB1RA_1RE1RC_---0LD_1RA1LD_0LF0LF_0LG1LF_1RA0LG`.  All 14 wires have a job.  It is not an edit of any machine we have read.

Tests (look.py; run lengths at the far-left blank cell):
    (3 6) -> (6 4) -> (9 2) -> (12)              pay 2, gain 3
    (12) -> (3 13)                                the lone block becomes the payer of a new block
    (3 13) ... -> (21 1) -> HALT                  13 is odd: the number test fires
    (9_ 3) -> (12 2) -> (3 10 2)                  the payer is empty: the next store pays 1 and the old block lands as the payer
    (3 7) ... -> (12 1) -> HALT                   odd payer
From a blank tape, started in A:  (3 4) -> (9) -> (3 10) -> (18) -> (3 19) -> ... (30 1) -> HALT at step 641 with 33 ones.
So from a blank tape it starts itself, multiplies, lands the block as a payer, and halts on its own number test: 9, 18, then 19 is odd.
It is small because of its constants (a lone block w lands as w+1), not because a part is missing.
Not yet in it: the overflow (a lone number becoming a row of levels); it has two levels and whatever is laid behind.

## Its near neighbours (22 Nov): can the constants be shifted so the number test fires later?

Every table within two wire changes of the from-scratch machine (57,214), from a blank tape, 5,000,000 steps:
14,809 halt (14,802 before step 1,000; the latest at step 6,528 with 106 ones), 10,825 run off an 8-million-cell tape, 31,580 still run.
Of those still running about 12,800 are one solid growing block, about 18,100 only short words, and 1,835 keep two or more runs with
a block of 100 cells or more (the engine is still there).  Those 1,835 for 1,000,000,000 steps: 0 halt, 925 run off the tape, 910 still
running (804 of them with just 2 runs).
Result: no late halt.  Shifting constants by one or two wires either lets the test fire at once or removes it.  The machine as formed
is a working two-level engine; what would make it big is the part it does not have yet - a row of levels (the overflow).
