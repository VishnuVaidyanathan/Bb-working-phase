# Designing from a layout (our own, not cut from any champion)

Method: draw a layout, then add one rule at a time as loose pictures made from the rule alone,
and ask `story/free` which tables play them. When a step fails, write down why before changing it.

## Layout 1

Tape `[0] 1^w 0 1^b 0 1^c ...` : the head rests on the blank cell left of the block being built (w).
Stores stand in a row to the right, each one 0 apart. The nearest store is the one being eaten.

| Step | Rule | Result |
|---|---|---|
| 1 | round: (w, b) -> (w+K, b-1) | fits in 3 states: 5 tables for K=2, 3 tables for K=3 (files here) |
| 2a | promotion with a bite of 2: (w, empty, c) -> (fresh F, w+3, c-2) | no table in 4 or 5 states, for K=2,3 and F=1,2, even with 7 head turns allowed. 6 and 7 states not tried yet. |
| 2b | promotion with a bite of 1: (w, empty, c) -> (fresh 1, w+2, c-1), K=2 | 8 tables in 5 states (`layout1_round_promotion_bite1_5_states.txt`) |

Seen by running those tables on a tape where the first store runs out (thought experiment): every one
plays the round correctly and then, at the double 0, either runs away or stops on an unused wire.
`1RB1LA_1RC1RB_---0LA` (K=2) uses 5 wires, and its one unused wire (C reads 0) is exactly
"I crossed the gap and the store is empty". That wire is where rule 2 goes.

## What the eight 5-state engines do on a bigger tape (thought experiment, `play.py`)

Start (1, 2, 3, 2). All eight give the same life:

    1 2 3 2 -> block 5 -> 1 7 2 2 -> block 15 -> 1 17 1 2 -> block 35 -> 1 37 _ 2 -> block 75, and now two stores are empty at once

- The block doubles for every cell of the store in front, and the store behind pays 1 at each promotion.
- The same rule works at every level without a separate picture for each level.
- At the wide gap (two empty stores) they differ: four treat it as one more promotion (1 79 or 1 80) and then run away at the
  end of the tape, three run away at once, and `1RB1LA_1RC1RB_1RD0LA_---0LE_1RC1LE` stops on its one unused wire, D reads 0.
- From a blank tape none of them is a machine: seven run away or stop at once, one is a plain bouncer.

Left over for the next rules: 2 states and the wire D0.

Why 2a failed: not known yet. A bite of 2 probably needs one more state to remember "one eaten, one to go".

## Layout 1, rule 3: two stores empty at once (the wide gap)

Rule: (w, empty, empty, d) -> (fresh 1, fresh 1, w+3, d-1). The block becomes the deeper store, the store behind pays 1, two fresh ones start.

| States | Tables playing round + promotion + wide gap |
|---|---|
| 6 | none |
| 7 | 2 (`layout1_three_rules_7_states.txt`) |

Thought experiment on (1, 1, 1, 3, 2): 1 5 _ 3 2 -> 1 1 14 2 2 -> 1 5 13 2 2 -> 1 13 12 2 2 -> 1 29 11 2 2 -> ... -> 1 2045 5 2 2 ...
So the middle store doubles for each cell of the deep store, and the deep store is reloaded from the big block: three levels (a tower).

**Why layout 1 fails as a machine**

- Both tables use all 14 wires. Nothing is left for a halt.
- From a blank tape both run off the tape. There is no opening.
- The cost: the round took 3 states, the promotion 2 more, the wide gap 2 more. Every rule needed states of its own.

**What to do differently**

- Rules must share states. One rule for "the store in front is empty" at every depth, not one per depth.
- The halt must not need a wire: it has to be a leftover (a remainder) seen by a wire that is otherwise on the river.
- The opening must be one of the rules acting on a blank tape, not a rule of its own.

## Layout 2, step 1: one rule for every depth

Same row of stores as layout 1. The promotion is asked for at two depths with the same shape:
(w, empty, c) -> (1, w+2, c-1) and (w, empty, empty, d) -> (1, w+3, d-1): whatever the gap, the next real store pays 1.

| States | Tables playing round + promotion at both depths |
|---|---|
| 5 | 1: `1RB1LA_1RC1RB_1RD0LA_1RD0LE_1RC1LE` |
| 6 | 84 |

The 5-state table is the layout 1 engine with its free wire set to "D reads 0: write 1, go right, stay D".
So the rule for every depth is one wire: keep filling zeros until a store is found. Layout 1 needed 7 states for two depths; this needs 5 for all depths.

**Why this is still not a machine**

- When nothing at all is left, D fills zeros for ever. Looking costs nothing, so the machine never learns that the tape has ended.
- From a blank tape it runs away for the same reason.

**What to do differently**

- The end must be found by the block running out, not by seeing blank tape: every look past an empty store must cost the block a cell
  and leave a mark behind. Then "nothing left" ends by itself, and the marks are the next stores.

## Layout 2, step 2: the gate, worked out by arithmetic before looking for a table (`fate.py`, `life2.py`)

The 5-state engine was run on a row of n equal stores until nothing was left (thought experiment), to get the ones on the tape T(n).

| Stores made by the cut | T(n), n = 1, 2, 3 ... | Leftover of T(n) |
|---|---|---|
| size 1 (cut by 2, stripes) | 4, 7, 16, 34, 70, 142, 286 (then 2T+2) | mod 2 always 0, mod 3 always 1: **the gate is dead** |
| size 2 (cut by 3, pieces 110) | 5, 10, 44, 180, 724, 2900 (then 4T+4) | mod 3 goes 2, 0, 1, 2, ...: **the gate is alive** |

Failure and reason: cutting by 2 gives a leftover that never changes, because doubling keeps the block's parity. A search for such tables was stopped.
Lesson: the cut's divisor must not divide the growth. Cut by 3 with growth 4 per store works (4 = 1 mod 3, so the leftover steps by 1 each layer).

Life with stores of 2, cut by 3, by arithmetic (n stores -> T(n)+J cells -> n' = (T+J)//3 stores, leftover = gate):

| Start | Block grows before the cut | Halt on leftover | Leftovers by layer | Falls in layer |
|---|---|---|---|---|
| 1 store | +1 | 1 | 0, 2, 0, 0, 1 | 5 |
| 3 stores | +1 | 2 | 0, 0, 1, 1, 2 | 5 |
| 4 stores | +2 | 0 | 2, 1, 2, 1, 0 | 5 |
| 2 stores | +0 | 0 | 1, 2, 1, 0 | 4 |

In the first row the stores go 1, 2, 3, 15, about 250 million, and the fall comes with about 4^(250 million) ones.
So if a table exists for this story, it is a big halting machine.

Engines with other numbers also exist (round +K per cell, fresh block F; round + promotion at every depth):
K=2 F=1: 1 table in 5 states, 84 in 6. K=2 F=2: 1 and 57. K=2 F=3: 0 and 7. K=3 F=1: 0 and 33. K=3 F=2: 0 and 42.

## Layout 2, step 3: the whole story in 7 states - fails

Pictures: round, promotion at depth 1 and 2, and the cut by 3 from the right end when four zeros are met (no halt yet).
Searched over every 7-state table, for the block growing 0, 1, 2 or 3 cells before the cut:

| Version | Tables |
|---|---|
| clean (one resting state for every rule) | none, for all four |
| loose (free resting states after a promotion and after a cut, first rounds drawn through the seam) | none, for all four |

(An earlier run of the clean version had a wrong cut picture and was thrown away.)

What the loose version showed: without the cut it finds the same engines as before (1 in 5 states, 84 in 6). So the closed seams were not what stopped it.

**Why it fails (my reading, not proved)**

- Each search died after the same number of steps whatever the cut was asked to produce. So it fails before the cut's shape matters:
  it fails at *knowing that nothing is left*.
- In this layout an empty store and the end of the tape look the same (zeros). To tell them apart the head must count zeros, and counting costs states.
  Then the cut needs a loop of 3 on top. Engine 5 + counting + cut does not fit in 7.

**What to do differently in layout 3**

- "Nothing left" must be seen in one look, as in BB5 (the cell after the block is a 1 if a piece is there, a 0 if not).
  So a used-up store must not leave a hole that looks like the end.
- The cut must not be a loop of its own. It has to ride on a walk the machine already makes.

## Layout 3: our own tower, with the gate found by rearranging, not by adding

**What failed first.** Our tower machine's run was cut into about 460 short pictures (`towerpics.py`), and one ending type at a time was
turned into a halt by hand. Searched over every 7-state table: no table for ending type 0, 1, 3 or 4.
Reason: those endings differ only in counts. With every rest of the tower fixed, no arrangement of 7 states can see them.
(Two earlier runs of this search were invalid because my picture maker left the halt pictures out; they are not counted.)

**What the tower can see** is the pair of endings that use the road b3 (types 0 and 2). A halt there needs one spare state as a tripwire:
the ticket wire goes into C; C on 0 does what B did; C on 1 halts. From the usual start that falls in layer 2 with 27 ones.

**The change that worked: start somewhere else.** By our gate arithmetic (`flow/tower_gate_arithmetic.py`), the layer in which the b3 ending
first comes depends only on the first layer: at best layer 5, from a first layer of 1 ticket starting in E.
The same table started in state D on a blank tape gives exactly that first layer (at step 11). A table started in another state is just
another machine, so after renaming the states:

    1RB0LC_1RD1RE_1LF1LA_1RC1LF_1LF1RZ_1RG1LD_0RA1RG

| Check | Result |
|---|---|
| our arithmetic, before running anything | layers of 1, 6, 18, 91 and 3,145,722 tickets; the fifth ends with b3: halt |
| Shawn Ligocki's Quick_Sim (flags -r, exp-linear-rules, exp-meta-linear-rules) | "Turing Machine Halted", 3*2^629147 - 15 ones, about 10^189,392 |
| direct run from a blank tape | no halt in 3 billion steps, 75,550 ones (as expected: the fall is far beyond a direct run) |
| Quick_Sim without -r | still climbing past 10^34,800 after 5 minutes, not finished |

Not checked by a second simulator. The halting size rests on Quick_Sim and on our own arithmetic agreeing.

Lessons:
- A gate cannot be bolted onto a machine whose every rest is fixed, unless the machine can already see the difference.
- What can be changed freely is where the machine enters its own cycle. The start state is a free choice, and it moved the fall from layer 2 to layer 5.

## Letting the tables arrange themselves (one wire, several jobs)

Instead of drawing every rule, only the round and the promotion were drawn, in 6 states, and each of the 325 tables that play them
was then run on a tape with deeper gaps to see what it does there by itself (`emerge.py`, thought experiments).
The tables fall into about 40 groups. Most run away or merge the stores (flat). A few do something deeper:

| What happens at a wide gap | Tables |
|---|---|
| runs away | about 190 |
| stops on an unused wire | about 30 |
| the stores behind are merged into one (flat) | about 10 |
| the store behind is reloaded with a small number and the last one pays | about 45 |
| **two fresh stores start and a middle store counts down while the first doubles: 1 1 8 1 2 -> 1 5 7 1 2 -> 1 13 6 1 2 -> 1 29 5 1 2 ...** | 1: `1RB0LE_0RC0RB_1RA0LD_1LD1LA_1RC1LF_1LF1LE` |

The last table is a stack that the search arranged by itself in 6 states (our hand-drawn three-level stack needed 7 and all 14 wires).
Its wires are shared: walking right it wipes the block and walking left it writes it back, and it crosses a wide gap by repeated trips,
leaving a mark where it started. Its rules are not worked out yet (`rules6.py` has the first thought experiments); in several cases it runs away to the right.

Also settled here: no 7-state table plays our hand-drawn three-level stack and halts when all three stores are empty
(only two tables play that stack at all, and both use every wire).

## Built by hand: a stack that works at every depth, with wires sharing jobs

Basics taken from reading how the champions load a wire: a state is one motion plus one question, and the answer must already be on
the tape. Built wire by wire and checked on small tapes after each wire (`play.py`, `turns.py`).

    1RB1RG_1RC1RB_0LF0LD_0LE1LD_0RA1LD_0RA1LF_---0RB        (7 states, 13 wires, G0 free)

| State | Motion | Question at the end |
|---|---|---|
| A | start right | 0: start a round (grow by 1). 1: this cell stays as a mark |
| B | walk right over the block | at the 0: fill it and let C look |
| C | look past the block | 1: eat it and go home. 0: the store is empty, make an empty trip |
| D, E | walk home, stepping over single 0s | two 0s in a row: this is the far left, turn |
| F | walk left over the block only | at its left end: hand over to A to leave a mark |
| G | after the mark | 1: wipe it (the gap after the mark). 0: the block is used up - **the end** |

First try failed: the mark was written on the cell where the round grows, so the next round swallowed it.
Fix: the mark is cut out of the block itself (first cell stays, second is wiped), and the walk home steps over single 0s,
so one home walk serves both the round and the promotion.

Thought experiments: (3, empty, 3) -> 1 4 2;  (4, empty, empty, 3) -> 1 1 4 2;  (5, three empty, 2) -> 1 1 1 4 1;
then 1 1 1 4 1 -> ... -> 9 _ _ 4 1 -> 1 1 9 3 1. One fresh store per empty level, the level below the payer reloaded with the block:
the stack rule at every depth. A block with nothing behind it always ends on G0, having turned itself into w+2 marks.

With G0 = 0LD (walk home: the marks become the next row, one level each):

    1RB1RG_1RC1RB_0LF0LD_0LE1LD_0RA1LD_0RA1LF_0LD0RB

From a blank tape: a row of 2 marks at step 13, a row of 5 marks at step 77, then a five-level stack that is still running after
40 million steps (stores 2070, 5108, 3058, 3066). It has no halt wire, so as built it never halts. Quick_Sim crashes on it.
With G0 = halt instead, every start state halts within 16 steps, because a blank tape is already "nothing left".

Open: the gate. All 14 wires are in use and the end always comes the same way (the block passes through every size), so there is no leftover to hang a halt on yet.

## First compression by hand: 7 states to 6

Reading the digit table of the hand-built stack, five wires carried only one job each (digits 4, 8, 9, a, c), and the end wire (c) was used twice in 10 million steps.
Digits 8 and a did the same thing in two different states ("write 0, right, A"). Letting those two states be one:

    1RB1RG_1RC1RB_0LF0LD_0LF1LD_------_0RA1LF_0LD0RB        (6 states, 12 wires, state E free)

Checked: the same rows on every hand tape tried, and from a blank tape the same 28,068 ones after 300 million steps.
The walk home over the marks is now a loop of wires that already existed (6, b, a, 1, c): the end wire c also hops over one mark,
so it is used 34 times instead of 2. Jobs per wire 2.6; digit 3 carries 6 jobs and digit b carries 5.
The end of a layer is still one fixed sequence (d 2 4 b a 1 c), the same every time, so there is still no leftover for a gate.

## A gate built by hand on the 6-state stack: works on small tapes, dead by arithmetic

Idea (from Pavel's words b610 / b6110, where one wire takes a bite of 1, 2 or 3 and the tape decides): make the look cost the block
two cells, so that an odd block and an even block end on different wires. The mark is now two cells (A keeps one, G keeps one, E wipes the next):

    1RB1RG_1RC1RB_0LF0LD_0LF1LD_0LD0RB_0RA1LF_1RZ1RE        (7 states, halt on G0)

| Thought experiment | Result |
|---|---|
| block 4, 6, 8 with nothing behind | refills: rows 2 2 2, 2 2 2 2, 2 2 2 2 2 (one level per mark) |
| block 5, 7, 9 with nothing behind | halts on G0 |
| (5, two empty, 3) | 2 2 3 2 (the stack rule still holds, fresh stores are 2) |

From a blank tape: rows 2 (step 13), 2 2 (step 48), 2 2 2 2 (step 165), then 2 6 1 2 -> 2 14 _ 2 -> 2 2 28 1 -> 2 6 27 1 -> ... ;
no halt in 3 billion steps (stores then 16496, 57287, 14, 1).

**Why it will never halt (arithmetic, before any longer run):** every step changes the block by an even amount -
a round adds 2, a look takes 2, a fresh block is 2. So the block is always even and the odd ending never comes.
It is the same mistake as cutting by 2 in layout 2: the gate's divisor divides the growth.

**What to change:** something must change the block by an odd amount a varying number of times (a round that adds 3, or a bite of 2 with its leftover).
Each of those needs one more wire than this table has free.
