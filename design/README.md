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

## Stepping stone in 8 states: the gate is alive, but fires at the first end

To make the block's parity change, the round was given one more write at the left turn (A0 = 1LH, H0 = 1RB), so a round adds 3:

    1LH1RG_1RC1RB_0LF0LD_0LF1LD_0LD0RB_0RA1LF_1RZ1RE_1RB---        (8 states, one wire unused)

| Thought experiment (`hand.c`) | Result |
|---|---|
| (3, empty, 3) | 2 4 2, then the block goes 5, 8, 11, 14: a round adds 3 |
| block 4, 6, 8 alone | halts at once |
| block 5, 7, 9 alone | refills: rows of 4, 5, 6 stores of 2 |
| block 3 alone | climbs, then **halts at step 8,516 with 96 ones** |
| block 5, 7, ... 21 alone | still climbing after 2 billion steps (stores 25676, 60331, 82, 1, ...) |

From a blank tape it halts at step 18 with 4 ones, for every start state and every choice of the unused wire (264 machines):
the first block a blank tape gives has the halting parity.

So the gate now depends on the arithmetic, as wanted, but the opening enters at the worst place. Same lesson as the tower:
what matters is where the machine enters its own cycle. Not worked out yet: the parity arithmetic of the stack (when the first odd leftover comes for a given first block).

## The 8-state stack as arithmetic, and its fate for each first block

Rules read off thought experiments (`stack8.py`), block w and a row of stores:

- round: (w, s) -> (w+3, s-1)
- store in front empty, g empty levels before a payer d:
  if w+3 > 2g: g fresh stores of 2 (the first is the new block), the old block becomes w+3-2g, the payer pays 1;
  if w+3 = 2k <= 2g: the block becomes exactly k fresh stores, nobody pays;
  if w+3 is odd and smaller than 2g: HALT
- nothing behind: w odd -> a new row of (w+3)/2 stores of 2; w even -> HALT

The fresh block is 2 and a round adds 3, so the block's parity at the end of a row is the parity of the number of promotions in that row.

Fate for each first block. To get a size, Shawn Ligocki's Quick_Sim was used as a calculator: a few start-up states were put in
front of the table to lay the first block and hand over (`stack8_with_startup_states.txt`). **These are not 7- or 8-state machines.**

| First block | Our arithmetic | Real table, direct run | Quick_Sim (with start-up states) |
|---|---|---|---|
| 0 (a blank tape) | halts at once | halts at step 18, 4 ones | - |
| 1 | row of 2, halts, last block 8 | halts at step 172, 12 ones | halted, 12 ones |
| 3 | row of 3, halts, last block 92 | halts at step 8,516, 96 ones | halted, 96 ones |
| 5 | row of 4; too long to follow by counting | still climbing after 2 billion steps | **halted**, (3 + 7*3^((-5 + 7*3^92)/2))/2 ones: between 10^^3 and 10^^4 |
| 7 | row of 5; too long | still climbing | reached about 10^^10^^10^^3, then the tool could not work out odd or even ("Cannot mod Iterated_Math by 2") |
| 9 | row of 6; too long | still climbing | reached about 10^^^10^^^10^^10^^10^^3, then the same |

So the design does stack towers: each extra store in the first row adds a level, and with a first block of 9 it reaches three-arrow sizes.
Whether it halts for 7 and 9 is not known: the gate asks whether a number of that size is odd, and the tool cannot answer.

Open: (1) the opening - a blank tape gives first block 0; (2) 8 states to 7.

## Opening: choosing the numbers before the table (stackgen.py)

Boots read side by side (first digits from a blank tape): Jeff `02468bba1d2468ba1c47698...`, Pavel `025247946103b611...`,
BB5 `02461590247777603333332461...`. Each champion walks through its 0-wires in order and its ordinary rules make the
first small rows; no special opening part. S8 reads `0e324bbba1d924ba1` and halts at step 18.

`stackgen.py` follows the stack design from a blank tape by arithmetic with three open numbers: K (cells a round adds),
m (size of a fresh store), RH (leftover that halts). Tested against S8 (K=3, m=2, RH=1: halts at once - agrees).
Result (arithmetic only, no table yet): if K and m share a divisor the halt can never fire (dead gate, same reason as S7).
Choices that do not die at once and are not dead are listed by the script.

## Transcript first (user's direction, 20 Nov): write the long transcript with 14 digits, fix bugs after

8-state stack in digits (first block 5), 15 digits in use:
round `6 a 0 e 3(n) 2 5 7(n+2)`, cut `2 4 b(n) a 1 d 9 3(n-3)`, hop over a mark `b b a 1 d 8 7 7 6`, halt `a 1 c`.
Digit e (H0) has one job only: it stands between 0 and 3 and writes the second new cell.

First 14-digit try: let digit a (F0) write a 1 when it turns, so digit 3 can stand where e stood (A0=1LB):
`1LB1RG_1RC1RB_0LF0LD_0LF1LD_0LD0RB_1RA1LF_1RZ1RE`. Round becomes `6 a 0 3(n) 2 5 7(n+1)`, block still +3 a round (tested, hand tapes).
Bug: digit a also turns the head at every cut, so it fills the gap between marks; the marks never form, the block is cut down
2 at a time and the machine halts small (blocks 0..9: 12 to 114 ones). To fix next.

## A 7-state stack from a blank tape (20 Nov, evening)

Among the 7-state tables within two wire changes of the hand-built stack (parked list), read by their stores:
`1RB1RG_1RC1RB_0LF0LD_1LC1LD_1LD0RB_0RA1LF_1RZ1RE` (hand stack with A0=1RB, D0=1LC, E0=1LD).
From a blank tape (tested, real run, 30 million steps, 5,852 home visits, arithmetic agrees on all of them):
block 0 -> 4 -> row [2,4] -> ... -> block 848 with nothing behind -> a row of 424 stores (423 of size 2 and one of 4).
Rules: round +3; fresh stores of 2; nothing behind: block odd -> HALT, block even w -> w/2-1 stores of 2 and a last store of 4.
A row of 424 stores means about 422 arrows at its end (Jeff Ketchersid's champion: 20).
BUT (arithmetic, calc/t7.py): the block at the end of such a row is always a multiple of 4 (rows of 0..24 stores of 2 plus a 4),
so the halt at the end of a row never fires. This table most likely never halts. It shows the engine fits in 7 states and
boots itself from a blank tape; it needs a gate that can fire.
112 more tables of the same family with a halt and a big store on the tape: stack_like_7_state_112_tables.txt (being run).

## Reading the 7-state stack's gate by arithmetic (20 Nov, night)

Sift of all 57,577 tables within two wire changes of the 7-state stack (halt anywhere): 16,042 halt small (longest 4,211 steps),
26 keep a big store with a row; calc/learn.py finds no big halter among them. Searching around it does not give a halt.

Why (arithmetic, engine "round +3, stores of 2"): the block at the end of a row is odd exactly when the row's last store is odd.
* last store even (0, 2, 4): every row ends even -> never halts (the 7-state stack has last store 4).
* last store odd (1, 3, 5): every row ends odd -> halts at the end of its FIRST row, with (stores in that row - 2) arrows.
A cut into stores of 2 has only two endings (block even / block odd). With one of them the halt, every row is treated alike.
To pass a small row and halt on the big one, the cut needs three endings: stores of 3 (as the gate study found), i.e. two more wires
than the 14 this table uses - or a halt that looks at something else than the cut ending.

## Store-of-3 versions of the 7-state stack (loose, 20 Nov night)

Engine wires of the 7-state stack kept; cut made one cell longer (state H: `1 d f 9`), three cut endings E0/G0/H0 left open.
* 8 states, round +3: 50 stack-like tables with rows of 3s from a blank tape; none can halt (round 3 and store 3 share a divisor).
* 9 states, round +4 (A0=1LI, I0=1RB): 29 stack-like; 8 judged never halts, the rest no verdict.
* 10 states, round +5 (A0=1LI, I0=1LJ, J0=1RB): 138 stack-like. calc/learn.py (rules read off the tape, in-row arithmetic agreeing with
  about 2,090 real home visits each): 7 tables HALT at the end of their first big row, e.g.
  `1LI1RG_1RC1RB_0LF0LD_1LC1LD_0LB0RB_0RA1LF_0RD1RH_1RZ1RE_1LJ---_1RB---` : blank tape -> big row of 95 stores -> halt, about 93 arrows.
  14 more survive it and at the tower-sized row halt or not by the row length.
  Status: tested by our arithmetic only. Not confirmed by a simulator (93 arrows is beyond what Quick_Sim reaches here). Not candidates (10 states).
Files: store3_round*_verdicts.txt.

Later the same night (learn.py now accepts a first big row of more than 8 stores):
* 8 states, round +2 (A0=0RB), stores of 3, blank tape: 6 tables HALT at the end of their first big row, e.g.
  `0RB1RG_1RC1RB_0LF0LD_1LC1LD_0LA0RB_0RA1LF_0RD1RH_1RZ1RE` : rows [2] -> block 5 -> [3,2] -> block 39 -> row of 14 stores -> halt, about 12 arrows.
  (round +2 behaves like round +5 when counted in threes: step 2x+1.)
* 9 states, round +4: two tables halt at the end of rows of 12 and 13 stores (10 and 11 arrows).
All "tested by our arithmetic only". File: store3_8_and_9_states_verdicts_short_rows.txt.

Longer row in 8 states? (same night)
* All 1,211 non-halting round +2 tables run to 20 million steps: 71 show a row of 3s; the same 6 halt (rows of 13 or 14 stores), 2 never halt,
  63 have no row longer than 8 stores. Starting in any other state gives the same rows. So 14 stores (12 arrows) is the most this family gives.
* The row length is set by the multiplier: round +2 gives 5 -> 39 -> 14 stores; round +5 (10 states) gives 95 stores.
* Ways tried on paper to add home cells without states: C0 writing (A then lands on a 1 and starts a cut), F0 writing (fills the gap between
  fresh stores - the old bug), A0 sent left into D, B or C (runs away to the left). One state can write two cells (I0=1RI, I1=1RB), not more.
