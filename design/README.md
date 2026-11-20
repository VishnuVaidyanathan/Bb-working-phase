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
