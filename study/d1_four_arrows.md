# D1: a 4-arrow machine read in full (working notes, 15 Nov 2026)

`1RB1RD_1LC0RD_0LG1LD_1RA0RE_1LF1LA_0LC1LE_1RZ0LE`, found by Andrew Ducharme (BB(7) page of the bbchallenge wiki).

Sources for this reading: Shawn Ligocki's Quick_Sim, which runs the machine to the halt in under a second and prints the
rules it proves (`-r --exp-linear-rules --exp-meta-linear-rules --no-steps --verbose-prover`); and plain runs of the first
1.5 million steps. The five rules below are the tool's proved rules, rewritten in our words. The reading of the run as a
whole is mine, from the tool's log; it is not proved here.

## The tape

Everything is on the left of the head. Numbers are stripes, in two phases: `(10)^x` and `(01)^x`. A `11` is a separator.
At the end of the big run the tape is five numbers in a row:

    (10)^m 11 (01)^k (10)^h 11 (01)^e 11 (01)^f   [head]   10

## The five rules (one per level)

| level | counter | what one round does |
|---|---|---|
| 1 | | the basic sweep: a stripe gives 1, the block gains 3 |
| 2 | e | e -> e - 1, f -> 3f + 11 |
| 3 | h | h -> h - 1, and f -> (5 * 3^(3f+14) - 11)/2. This is level 2 run until e is used up, with e reloaded from f. |
| 4 | k | k -> k - 1, and f -> level 3 repeated (5 * 3^(3f+15) - 9)/2 times, starting from 2 |
| 5 | m | m -> m - 1, and f -> level 4 repeated a number of times that itself comes from level 3 |

Every level is the same idea: **a counter loses 1, and the level below is run as many times as the block says.**
When a counter is used up, the counter to its left loses 1 and the used-up counter is loaded again from the block.
Level 2 is a power, level 3 a tower, level 4 three arrows, level 5 four arrows.

There is no remainder gate. The run ends when the leftmost counter is used up.

## The run from a blank tape (from the tool's log)

| phase | tape | what happens |
|---|---|---|
| boot | `01 11 (10)^4 11 (10)^3 11 (01)^8` | the boot has laid a small stack: counters 4 and 3 and a block of 8 |
| 1 | the counter 3 goes 3, 2, 1, 0 | each step puts the block in the exponent: the block becomes about 3^(3^(3^(3^21))) |
| turn | `(10)^M 11 01 10 11 ...` | that tower M becomes the leftmost counter of a deeper stack, with fresh small counters to its right |
| 2 | m goes from M down to 1 | each step is one use of the level 5 rule |
| end | m = 1 | halt, with about `10↑↑↑↑...` ones (4 arrows) |

So the depth of 5 is not five separate rules in the table. The table has one way of handling "this counter is used up:
take 1 from the one on its left and reload". The depth comes from how many counters are standing on the tape, and that
comes from the small stack the boot lays (4 and 3) and from the turn after phase 1.

## Words (decimal transcript)

- Fillers: the four-digit word `0379` walks right over a stripe; the pair `8b` walks left.
- Round: `0378a4d (8b)^k 9 (0379)^k 036025 79 0379 036025 79`, with k growing by 3 per round (seen: 4, 7, 10, 13, 16, 19).
- The rare wire `1` (A reads 1) is used once per level-2 round, in `9 1 79`.
- All 13 wires have appeared by digit 56. The boot is made of the same words at small size
  (`0378a4d9`, `0378a4d8b9`, `0379`, `036025`), as in the other machines.

## Compared with the others

| | D1 | Pavel's (P) | Jeff's (J) |
|---|---|---|---|
| numbers kept as | stripes, two phases, `11` between | stripes, a single `1` between | solid blocks with gaps |
| counter loses | 1 | 3 | 2 |
| gate | none: ends when the leftmost counter is used up | remainder expected | parity |
| depth on the tape | 5 | about 12 | 19 |
| what sets the depth | the stack the boot lays (4, 3) and one turn | 14 units laid by the boot | 19 units laid by the restart |

D1 is the plainest of the three: a nested countdown with no luck in it. If its stack were one counter deeper at the
start, the same table should give one more arrow. That is an inference from the rules, not something checked.

## Not done

- The boot written by hand, digit for digit.
- A test of the table on hand-made stacks of other depths. The runs are too long for plain running; it would need
  the tool to start from a given tape.
