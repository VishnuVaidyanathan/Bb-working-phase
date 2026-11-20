# Designing from a layout (our own, not cut from any champion)

Method: draw a layout, then add one rule at a time as loose pictures made from the rule alone,
and ask `story/free` which tables play them. When a step fails, write down why before changing it.

## Layout 1

Tape `[0] 1^w 0 1^b 0 1^c ...` : the head rests on the blank cell left of the block being built (w).
Stores stand in a row to the right, each one 0 apart. The nearest store is the one being eaten.

| Step | Rule | Result |
|---|---|---|
| 1 | round: (w, b) -> (w+K, b-1) | fits in 3 states: 5 tables for K=2, 3 tables for K=3 (files here) |

Seen by running those tables on a tape where the first store runs out (thought experiment): every one
plays the round correctly and then, at the double 0, either runs away or stops on an unused wire.
`1RB1LA_1RC1RB_---0LA` (K=2) uses 5 wires, and its one unused wire (C reads 0) is exactly
"I crossed the gap and the store is empty". That wire is where rule 2 goes.
