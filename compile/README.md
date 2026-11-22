# From the story to a table: story -> trips -> roomy table -> squeeze -> check  (22 Nov, night; Vishnu's question)

The gap so far: we know the story (the grammar: who hands what to whom), and we can run a table.  In between we either laid wires by
feel (and lost what was needed) or changed wires of finished tables (and got the same machines back).  This folder is the bridge.

1. STORY.  The rules on lists of numbers, as in engines/bench.py: round, payment, landing, new row, the tests.  Checked on paper and on
   the bench (odd/even algebra, exact short rows) before anything else.
2. TRIPS.  Choose a layout (how a number sits on the tape, where the head rests).  Every rule becomes one walk of the head: out from
   home, do its work, back.  A walk is a string of JOBS: run over a block, fill a cell, look, step over, erase, write, turn.
3. ROOMY TABLE.  Give every job its own state.  At each job ask the one question a state can ask - "is the cell a 1 or a 0?" - and
   write what must happen in each case (a case that cannot happen is left ---).  This is mechanical and may take 10 to 15 states.
   Nothing clever is done here, so nothing is lost.  The halt wire is written 1RZ.
4. SQUEEZE (squeeze.py).  Two states can become one when, for each symbol, the wires that are really used agree; an unused wire is
   free.  The tool tries every grouping of the states into 7 (or 8), keeps the ones with no clash, and checks that the squeezed table
   moves exactly like the roomy one, step for step.  All the overlaps we looked for by hand are groupings of this kind.
   If no grouping exists, the trips are changed (another layout, another order of jobs) - not single wires.
5. CHECK.  The squeezed table is written in tree normal form and run: on hand-made tapes against the story (the next home visit must be
   what the rule says: fit.c / home_visits.py), then from a blank tape against the bench visit by visit, then by Shawn Ligocki's
   Quick_Sim.  A table passes only if the real visits agree with the story.

First use of squeeze.py, on our own machines (1,000,000 steps each):
* the 9-state machine `1LI1RG_1RC1RB_0LF0LD_1LC1LD_0RD0RB_0RA1LF_1RZ1RH_0RE1RE_1RB---`: no grouping into 8.  Same for the other 9-state
  engine and for the 10-state machine into 9.  They are already as tight as their trips allow - which agrees with the wire counts.
* a trap the first run fell into, kept here as a warning: when the halt wire was treated as "unused" (it never fires in a million
  steps) the tool merged the halting state with another and returned an 8-state table that runs exactly alike - and has no halt wire
  at all.  The halt wire is now always kept.

## First roomy table (roomy1.txt) — result: tested

Story written as 13 states, one job each: round (+3, payer −1), plain payment
(payer pays 2, block lands +4), landing two levels deep (fresh store of 2,
block lands +5), halt on a payer left with 1.

- Hand tapes follow the story (tested, 7 tapes).
- Squeeze (`squeeze_tapes.py roomy1.txt 7`): 13 → 12 in 5 ways, 13 → 11 in
  3 ways (e.g. A+H and G+M), 13 → 10 in **0** ways.
- With two extra tapes outside what the table was built for, only 13 → 12.

Reason for the stop at 11: the plain return (E, F, G) and the deep return
(H, I, J, K, L) are two separate chains of trips. Each level of depth costs
its own states, so the table grows with depth instead of looping.

Lesson: the squeeze cannot fix the trips. The story must be written so that
one trip serves every depth (depth carried on the tape, e.g. by the width of
a gap), not one chain of states per depth. That is roomy table 2.

## Overlapping wires: what Jeff Ketchersid's machine shows (observed, `jeff/wires.py`, `jeff/door.py`)

Squeeze merges whole states. Overlap is stronger: the *same wire* works in
several jobs.

Observed in Jeff's machine (real run from blank tape):

- The round uses 9 wires in 6 states: A0 B0 B1 C0 D0 D1 E0 E1 F0.
- **All 9 are used again in every other job** (payment, landing, new row).
- The other jobs add only 4 wires: A1, F1, G0, G1. The halt is C1.
- Three round states only ever read one symbol in a round (A, C, F read 0).
  Their other half is free. We call a free half a **door**.

One payment (7; 0 52 …) → (1; 12 50 …), written as wires (`door.py`):
the head leaves the round wires only 7 times, each time through a door
(F1, or A1 then G1/G0), changes one or two cells, and falls back into the
round wires. The round wires do the rest on the changed tape.

So a job is not a separate trip. A job = the round's loop, run again on a
tape left in an unusual shape, plus a door of one or two wires.

Compare roomy table 1: the round used 6 wires in 4 states with one free
half; every other job had its own runners and its own way home (15 more
wires). That is why it stopped at 11 states.

### What makes overlap possible (rules we take from this)

1. A door exists where a round state expects one symbol and meets the other.
   A round with more one-symbol states has more doors.
2. The special moment in the story (front store empty, payer at 1, …) must
   itself cause that unexpected read. The tape shape is the signal.
3. Behind the door do very little: change a cell or two, then re-enter a
   round state. Never build a second runner or a second way home.
4. A job may pass through the round loop several times before it is done.
   Half-finished tape shapes between passes are fine if each one opens the
   next door.
5. The halt is a door too: one free half that only a bad shape can reach.
