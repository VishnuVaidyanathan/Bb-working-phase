# Pavel Kropitz's 7-state machine: the depth word and the gate

Machine: `1RB0RA_1LC1LF_1RD0LB_1RA1LE_1RZ0LC_1RG1LD_0RG0RF` (Pavel Kropitz).
Size by Shawn Ligocki's Quick_Sim: 2↑^11 2↑^11 3.

Everything here is **tested** by running the table (real run from a blank tape, or
hand-made tapes where said). Nothing here is proved. Tool: `tools/pavel_gate.py`.

## How to read the tape

Look at the tape each time the machine uses its gate wire (state G reading 0, digit `c`).

- Left of the head: stripe groups `(10)^m`, written as the number m, with `110` between them.
- Right of the head: a row of units, `101 (100)^k 101` = k units.

## 1. The depth word: x becomes 2x + 4 units

A lone group of x with no units, `11 (10)^x 1 [c] 101101`, becomes
`1101 [c] 101 (100)^(2x+4) 101`: the left side is emptied and 2x + 4 units are laid.

Tested on hand tapes for x = 1 to 14. In the real run this happens once, in the boot,
at step 256 with x = 5, giving 14 units at step 1028.

(The field notes guessed 3 x 5 - 1. That was a coincidence. The rule is 2x + 4.)

Jeff Ketchersid's machine does the same kind of thing with (3P - 1)/2.

## 2. Each unit becomes one counter

One unit is turned into one stripe group in 3 gate visits. After the 14 units are
used (step 8,266) the left side is 13 groups of 3 and a last group of 4. So the
depth word's 14 units become about 13 counters.

## 3. The engine: borrow 3, double the last group

With no units left, the last two groups (a, b) go to (a-1, b+2) at each gate visit,
until a is 0. So the last group grows by twice the group before it.

Then the machine borrows from the next group to the left. A borrow takes 3 from that
group, in two bites (2, then 1), and lays 2 units. The units become new groups and the
doubling starts again, one level deeper.

Seen in the real run: `3 . 12` -> `1, 14, 2 units` -> `0, 16, 1 unit` and later
`39 . 12` -> `37, 14` -> `36, 16`, and `36 . 36` -> `34, 38` -> `33, 40`.

This is the borrow-and-reload engine, the same family as Andrew Ducharme's 4-arrow
machine, with one counter per level (about 13 counters, 12 rule levels in Quick_Sim).

## 4. The gate: the counter modulo 3

Hand tapes with one counter c to the left of the working group:

| c | what the borrow does |
|---|---|
| 0, and nothing further left | halts at once |
| 1 | takes what it can, halts on the second bite |
| 2 | first borrow works, halts later without touching the group further left |
| 3 | goes to 0 cleanly; the next borrow comes from the group further left |
| 4 | goes to 1, then halts at the next borrow |
| 5 | goes to 2, then as c = 2 |

With two counters (d, c): c = 3 does not halt in 3 million steps and keeps growing;
c = 2, 4, 5 all halt, and for c = 2 the step count is the same for d = 3, 4, 5.

So a counter must be a multiple of 3 to be used up cleanly. This is the same law as
in the other machines: the gate is the counter modulo its own step (here 3).
The 13 counters laid by the boot are all exactly 3, so each is used exactly once.

## 5. What is not known

- Which of the two halting sides ends the real run: a later counter that is not a
  multiple of 3, or the borrow reaching the left end of the tape. Not determined.
- Quick_Sim's verbose proof for this machine was started and stopped: its output
  passed 2 GB before the halt. The 12 rules were not read from it.
- The depth word fires only once in the real run (in the boot). On the tapes tried,
  reaching the left end later gives a halt, not a second depth word.

## Compared with Jeff's machine

| | Jeff | Pavel |
|---|---|---|
| depth word | P -> (3P-1)/2 units | x -> 2x + 4 units |
| fires | once, mid-run (13 -> 19) | once, in the boot (5 -> 14) |
| a unit becomes | one use of the move | one counter of exactly 3 |
| counter step / gate | 2 / parity | 3 / mod 3 |
| engine | use once, join gaps, replant | borrow and reload |
