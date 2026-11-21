# One-wire changes of two machines we have read (21 Nov)

Machines: the gated holdout `1RB0LG_1RC0RA_1LD1LE_1LB0LC_0LF0RE_0LG0LC_0RA---` (from Polygon's list; row of 21, read in holdouts/g4)
and Pavel Kropitz's `1RB0RA_1LC1LF_1RD0LB_1RA1LE_1RZ0LC_1RG1LD_0RG0RF`.
nbrs.py makes every table that differs in one wire (715 each; when the halt wire is the one changed, the halt moves to each other wire in turn).

Result, from a blank tape (tested):
- 915 of 1,430 halt, every one within 2,000 steps (direct.c, 50 million steps).
- 515 keep running. Shawn Ligocki's Quick_Sim (batch.sh, 20 s each): 507 proved never to halt, 8 not settled (undecided_8.txt).
- Of the 8: three are the holdout's own stack again (the changed wire is not used), the rest grow slowly.
- Halting after a long run: 0.

So neither machine has a bigger halting machine one wire away.
