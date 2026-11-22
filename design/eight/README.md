# Crushing the 9-state machine into 8 states (22 Nov, night)

Count of wire-jobs (observed, 6,000,000 steps from a blank tape, 9-state TNF
`1RB1LF_1LC---_1LD1LC_0RE0RI_0LA1RE_1RZ1LG_0LH1LH_0LI0LC_1RD1RI`):

- 18 wires. B1 is never used. F0 is the halt. G0 fires **once**, at step 182.
- So in the long run the engine uses 15 wires + the halt = 16 = eight states.
  The ninth state is paid only for one job in the start.

Tested: put G's used half into B's free half (8 states):
`1RB1LG_1LC1LF_1LD1LC_0RE0RH_0LA1RE_0LH0LC_1RZ1LB_1RD1RH` -> halts at step
199 with 16 ones (the number test fires in the start).  Same for the other
TNF: `1RB1RG_1RC1RB_0LD0LH_0RE1LD_1LA1RF_1RZ1RA_0RH0RB_1LC1LH` -> halts at
step 25.  Started in each of the 8 states from a blank tape: all 16 halt
before step 202.

So: the engine fits in 8 states.  What is missing is a start that the
engine's own wires can make.  (Not proved that G0 never fires again later;
only observed for 6,000,000 steps.)

Running: nb.c - every table within two wire changes of the two 8-state
tables, from a blank tape, 2,000,000 steps.

## Neighbour test result (nb.c, 2,000,000 steps from a blank tape) — tested

Tables within two wire changes: 101,371 around each 8-state table.

| | around table 1 | around table 2 |
|---|---|---|
| halt before step 1,000 | 28,926 | 34,963 |
| halt later | 7 (latest step 74,414, 426 ones) | 31 (latest step 1,616,214, 2,753 ones) |
| running, a few large runs on the tape | 493 | 386 |
| running, junk (solid block or tiny pieces) | the rest | the rest |

The 879 with a few large runs, Quick_Sim (Shawn Ligocki) 12 seconds each:
545 proved infinite, 334 still running, 0 halt.

The 334 after 30,000,000 steps, by tape shape (show.c):

- about 180: block, store, and a small counter going down by 1 while the
  block triples (16, 15, 14, 13 … seen up to 1,000,000,000 steps).
  Example `1RB1RG_1RC1RB_0LD0LH_0RA1LD_1LA1RF_1RZ1RA_0RH0RB_1LC1LH`.
  One multiplication per unit of a small counter: an exponential, not a tower.
- about 70: the same kind, counter 31, 30, 29, 28.
  Example `1RB1LF_1LC1LF_1LD1LC_0RE0RH_0LA1RE_0LH0LC_1RZ1LB_1RD1RH`.
- 1 table lays a **row of stores that doubles in length** each time
  (2x3, 2x7, 2x14, 2x28, 2x82 …):
  `1RB1RG_1RG1RB_0LD0LH_0RE1LD_1LA0RC_1RZ1RA_0RH0RB_1LC1LH`. Not read yet.

Not decided: whether any of the 334 halts. Quick_Sim is running 25 minutes
on four of them.

## Longer Quick_Sim runs (23 Nov) — tested; corrects the note above

- Row-doubling table: 25 minutes, only rule level 1, about 27 million ones.
  Slow. Not a tower.
- The "small counter" tables are NOT just an exponential (my call above was
  wrong). Quick_Sim, 4 minutes each, from a blank tape, still running:

  `1RB1RG_1RC1RB_0LD0LH_0RA1LD_1LA1RF_1RZ1RA_0RH0RB_1LC1LH`
  ones between (10↑↑↑↑)^4 10↑↑↑ 10↑↑ 26150882525 and … 26150884051;
  the counter on the right has gone from 62 to 59.

  `1RB1LF_1LC1LF_1LD1LC_0RE0RH_0LA1RE_0LH0LC_1RZ1LB_1RD1RH`
  ones between (10↑↑↑↑)^4 10↑↑↑ 10↑↑ 10^21 and … 10^23; counter at 13.

  The numbers in brackets are Quick_Sim's lower and upper estimates.
- So: 8 states, started from a blank tape, four arrows reached, and one more
  four-arrow step for each unit of the counter (observed, 4 units).
- NOT known: what happens when the counter reaches 0 (halt, a new counter,
  or running for ever). Until that is read, these are not halting machines.
