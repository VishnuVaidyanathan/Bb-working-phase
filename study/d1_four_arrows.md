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

## The same table started from other stacks (checked with Quick_Sim, `d1_from_stack.py`)

The tool is run from a blank tape until the boot has laid its stack, `01 11 (10)^4 11 (10)^3 11 (01)^8`. The stack is
then changed by hand and the tool continues. Every run below reached the halt in about a second.
With the real stack (4, 3) the result is identical to the normal run.

| stack of counters | rule levels | size |
|---|---|---|
| 3 (one counter) | 3 | a power tower 19 high (1 arrow chain) |
| 5 (one counter) | 3 | a power tower 25 high |
| 1, 1 | 5 | 4 arrows |
| 2, 3 | 5 | 4 arrows |
| **4, 3 (the real machine)** | **5** | **4 arrows** |
| 4, 5 | 5 | 4 arrows |
| 8, 3 | 5 | 4 arrows |
| 4, 1, 3 | 7 | **6 arrows** |
| 4, 4, 3 | 7 | 6 arrows |
| 2, 2, 2, 3 | 9 | **8 arrows** |
| 4, 4, 4, 3 | 9 | 8 arrows |

- **Each extra counter in the starting stack adds 2 rule levels and 2 arrows.** One counter: towers. Two: 4 arrows. Three: 6. Four: 8.
- The values of the counters hardly matter. (1, 1) and (8, 3) are both 4 arrows; only the smaller terms change.
- Every one of these halts. There is no gate to get past.

So this table can run at 6 or 8 arrows. From a blank tape it runs at 4 because its boot lays two counters.
These are hand-made tapes: they show what the table can do, they are not machines from a blank tape.

## The boot, step by step (plain run, steps 1 to 505)

| steps | tape | what happens |
|---|---|---|
| 1 to 124 | `1110 1111 (10)^4 [1] 11` | first small pass: a stripe group of 4 is made |
| 126 to 142 | `111011 [1] 1^9 0001` | the 4 stripes are turned into a solid block of 9 (2 x 4 + 1), and one unit `001` appears on the right |
| 142 to 211 | `111 [0] 1110 (001)^4` | the block of 9 is turned into 4 units on the right, 2 cells per unit |
| 211 to 242 | `111 (10)^4 110 110 110 [1] 11` | the 4 units come back to the left as a stripe group of 4, the **first counter**, followed by three `110` marks |
| 242 to 341 | `111 (10)^4 11 (10)^4 [1] 111001` | the marks are worked off one at a time; behind the first counter a **second counter** grows |
| 341 to 505 | `111 (10)^4 11 (10)^3 1 (10)^9 0 [head]` | normal rounds have started: the second counter is already counting down (6, 5, 4, 3) and the block is growing |

At step 505 the tape is the one Quick_Sim shows as `01 11 (10)^4 11 (10)^3 11 (01)^8`.

What the boot is made of: the same three conversions the main run uses, at size 4.

    stripes (10)^k  ->  solid block 1^(2k+1)  ->  units (001)^k on the right  ->  stripes (10)^k on the left, plus marks

The first counter is the result of going once round this cycle. The second counter comes from the marks left behind.
The far left end `111` is never rebuilt.

## Turn or halt: there is no separate rule (checked with Quick_Sim, `d1_from_tape.py`)

The whole left side of the tape was replaced by hand at the moment the boot tape is reached, and the tool was run on.
`01`, `10` are stripe groups, `11` is the separator; the last `01` group is the block.

| left side of the tape | groups before the block | rule levels | size |
|---|---|---|---|
| `01^2` | 0 | 0 | 9 ones |
| `10 11 01^2` | 1 | 0 | 23 ones |
| `10^3 11 01^2` | 1 | 0 | 35 ones |
| `01 11 01^2` | 1 | 1 | 47 ones |
| `11 10 11 01^2` | 1, after a bare separator | 2 | 5 x 3^10 |
| `10 11 10 11 01^2` | 2 | 2 | one power |
| `01 11 10 11 01^2` | 2 | 3 | a power tower 7 high |
| `01^2 11 10 11 01^2` | 2 | 3 | 2 arrows |
| `01 11 10 11 10 11 01^2` | 3 | 5 | 4 arrows |
| `01 11 01 11 10 11 01^2` | 3 | 5 | 4 arrows |
| `01 11 10^4 11 10^3 11 01^8` (the real boot tape) | 3 | 5 | 4 arrows |
| `01 11 10^4 11 10^4 11 10^3 11 01^8` | 4 | 7 | 6 arrows |
| five groups | 5 | 9 | 8 arrows |

- The three cells `111` at the far left of the tape are themselves a group: a `01` stripe of length 1 and a separator.
  It is the last counter. The "turn" after phase 1 is this counter being used: an ordinary reload, not a special rule.
- When the leftmost group is used up and nothing stands to its left, the machine halts.
- **Rule levels = 2 x groups - 1, and arrows = 2 x groups - 2**, for stacks that begin with a `01` group.
  The real machine has 3 groups (the `111` end, the counter 4, the counter 3): 5 levels, 4 arrows.
- A stack that begins with a `10` group, or has only one group, stays small.

So the boot lays exactly three things: the `111` end in its first steps, the first counter from one trip round the cycle,
and the second counter from the marks. A 6-arrow machine of this kind needs a fourth group.

## Not done

- The boot written by hand, digit for digit.
- Why each group is worth two arrows and not one.
- A table whose boot lays four groups.
