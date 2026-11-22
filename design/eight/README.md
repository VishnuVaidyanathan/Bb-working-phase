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
