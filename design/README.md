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
