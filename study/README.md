# Study of big machines

| file | what it is |
|---|---|
| this page | five machines read side by side |
| [`catalogue.md`](catalogue.md) | 24 machines profiled: size, rule levels, base, divisors, storage, fillers |
| [`d1_four_arrows.md`](d1_four_arrows.md) | a 4-arrow machine read in full; each group on the tape adds two arrows |
| [`wire_jobs.md`](wire_jobs.md) | which wires do more than one job |
| [`late_wires/`](late_wires) | deep openings kept, late wires freed: about 82,000 tables, nothing new |
| [`machines.txt`](machines.txt) | the 24 tables with their ids |
| [`tools/`](tools) | the scripts |

## Five big machines read side by side (working notes, 15 Nov 2026)

Purpose: before imagining a new machine, read several big ones the same way: pieces on the tape, words,
rules, gate, boot. Digits: one per step, `2*state + symbol read`, `0-9` then `a b c d`.

How far each reading goes is stated for each machine. "Proved" = a Coq file in this repo or the one named.
"Tested" = checked by plain runs on the real run and on hand-made tapes. "Observed" = seen in the real run only.

| | machine | states | size | who |
|---|---|---|---|---|
| J | `1RB0RG_1RC1RB_0RD1RZ_0LE0LD_0LF1LE_1RA1LF_1LC0RB` | 7 | about 19 levels | Jeff Ketchersid (claimed champion) |
| P | `1RB0RA_1LC1LF_1RD0LB_1RA1LE_1RZ0LC_1RG1LD_0RG0RF` | 7 | 11 arrows | Pavel Kropitz |
| S | `1RB1RA_1RC1RZ_1LD0RF_1RA0LE_0LD1RC_1RA0RE` | 6 | 3 arrows | BB(6) champion; rules by mxdys |
| T | `1RB0LD_1RC0RF_1LC1LA_0LE1RZ_1LF0RB_0RC0RE` | 6 | 10↑↑15 (2 arrows) | Pavel Kropitz |
| B | `1RB0LG_1LC1LB_0RD1LE_1RE1RD_0RF0RE_1LA1RF_---1LB` | 7 | tower, never halts | from our cousins search |

Sizes of P, S, T are from Shawn Ligocki's Quick_Sim (it runs each of them to the halt).

## T: the 6-state tower (tested; opening written by hand, 570 of 570 digits, `tools/t15_boot.py`)

Tape `1 0^G [A reads 1] 1^n`: a gap of G zeros (the counter) and a block of n ones.

| when | what happens |
|---|---|
| G >= 4 (layer) | G -> G - 4, n -> 3n + 13 |
| G = 1 or 2 (reload) | G -> n + 1, n -> 7 |
| G = 3 (reload) | G -> n + 7, n -> 7 |
| G = 0 | **halt** |

Words: layer round `R(k) = 03 (b93)^k a 4(3k+3) 5`; reload `03 (b93)^k b9245` or `03 (b93)^k b8`; gate pieces `168`, `a5`.
The gate is **G mod 4**, and 4 is what a layer takes from the counter. The run visits the gate 15 times before G mod 4 = 0.
This is the same kind of machine as B, but its gate has a halting side.

## B: the base-4 tower (proved, `cousins/bb7/base4/Base4Tower.v`)

Layer: L -> L - 2, n -> 4n + 4. Gate (L = 0): L -> n, n -> 4. L is always even, so the gate has one side only: no halt.

## S: the BB(6) champion (proved; Coq with exact step counts in the BB5 repo, rules by mxdys)

Pieces: a header, an outer binary counter (a bit is `111` or `001`), a marker with q ones, a right block of b triples.

| level | what happens |
|---|---|
| tick | the inner binary counter goes down by one (with borrow) |
| epoch | the outer counter goes down by one; the right block becomes a new inner counter of b bits, so it needs 2^b - 1 ticks: b -> about 2^b |
| restart | outer counter is zero and q = 3a + 1: a new outer counter is loaded |
| halt | outer counter is zero and q = 3a |

Three levels, all fixed in the table: 3 arrows. The gate is **q mod 3**; q gains 2 (mod 6) per epoch.

## J: Jeff's machine (proved to halt; see `bb7/`)

Pieces: solid blocks of ones separated by gaps; a unit is `1100`.
One move works at any depth: `1^P 0^(2j) 1^Z -> (1100)^(j-1) 1^(3P+8-2j) 00 1^(Z-2)`.
Tripling P -> 3P + 6; a counter loses 2 per tripling; when a counter is used up two gaps join (one level up).
Gate: **parity** (a counter loses 2). Even: halt. Odd at the last cell: restart with (3P - 1)/2 units.
Boot: 2 pairs -> 7 pairs -> gate P = 13 -> 19 units. Level = number of units = 19.

## P: Pavel's machine (observed for 6 million steps; gate not read yet)

Pieces: the tape is **striped**. A number m is stored as `(10)^m`; numbers on the left are separated by a single `1`.
On the right there are units `100` (or `110`), between the marks `101 ... 101`.

Words: two-digit fillers `25` (to the right) and `ad` (to the left); a round is
`53 (ad)^k a c d a d b 6103b W 53b W 5 (25)^(k+1)` with `W = 6110252479`; a carry is `b61103` repeated once per unit.
The wire `c` (G reads 0) is used once per round, inside the `ad` filler.

What the run does (`tools/pavel.py`):

| step | left groups | units on the right |
|---|---|---|
| 102 | [1] | 1 |
| 255 | [5] | 0 |
| 1,027 | [1] | **14** |
| 8,112 | [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5] | 1 |
| later | [4 x 10, 1, a, x] | 0 or 1 |

- The boot lays 14 units. Each unit is then turned into one group on the left: 12 groups of 4 and a last one.
- The last two groups work as counter and block: a -> a - 3 while x -> 2x + 7 (seen: a = 40, 37, 34 ... and x = 5, 13, 37, 85, 181, 373, 757, 1525).
- When a is used up (a = 1), x becomes the counter of the next group to the left, and a fresh x starts at 5.
  So each group is one level. About 12 groups, 11 arrows.
- The counter loses 3 per round, so the gate is expected to be **mod 3**. Not checked.

## Side by side

| | T | B | S | J | P |
|---|---|---|---|---|---|
| numbers stored as | gap of zeros, block of ones | two blocks of ones | binary digits `111` / `001` | blocks with gaps, units `1100` | stripes `(10)^m`, units `100` |
| growth per round | x3 | x4 | x2 (binary) | x3 | x2 |
| counter loses | 4 | 2 | 1 (with borrow) | 2 | 3 |
| reload | block becomes the counter | block becomes the counter | block becomes the inner counter | two gaps join | block becomes the next counter |
| levels | 2, in the table | 2, in the table | 3, in the table | on the tape: 19 units | on the tape: about 12 groups |
| gate | counter mod 4 | none (always even) | q mod 3 | parity | mod 3 expected |
| halting side | G = 0 | none | q = 3a | even P | not read |
| boot | words at small size (by hand: 570 digits) | words at small size | a small epoch (27,965 steps) | words at small size (by hand: 319 digits) | words at small size; lays 14 units |

## What is common

1. **Two numbers do the work**: a counter that is spent and a block that grows by a fixed factor per unit of counter.
2. **Reload**: when the counter is used up, the grown block becomes the new counter. This one step is what turns
   exponential growth into a tower.
3. **The gate is the counter modulo its own step.** A counter that loses s per round can end on s different
   remainders; the gate is those remainders. Step 2 gives parity (J, B), step 3 gives mod 3 (S, P), step 4 gives mod 4 (T).
   A machine halts if one remainder leads to the halt wire and the run can reach it. B cannot: its counter is always even.
4. **Levels are either in the table or on the tape.** In the table: 2 or 3 at most (T, B, S). On the tape: as many as the boot lays (J, P).
   Both machines above 3 arrows store their levels on the tape, as a row of small units that the main loop turns into counters one by one.
5. **The boot is the machine at small size** in every case, and in J and P it decides the level: J lays 19 units, P lays 14.
   J: 13 -> 19 = (3*13 - 1)/2. P: 5 -> 14 = 3*5 - 1. (Observed; the likeness is not explained.)

## What differs, and so can be chosen

- How a list of numbers is kept on the tape: solid blocks with gaps (J), stripes with a separator (P), binary digits (S).
- The factor (2, 3, 4) and the counter step (1, 2, 3, 4), which sets the gate.
- Fillers: single digits (J, T, B) or digit pairs `25`, `ad` (P). Pair fillers are what read and write stripes.
- When the gate wire first appears: early in J (digit 18), last in P (digit 103).

## For a machine of 6 or 7 arrows

It has to be of the "levels on the tape" kind. The count needed is small: a boot that lays about 8 units.
P shows a second way to do this beside J: stripes and pair fillers, with a carry that turns one unit into one group.

## Files

- `tools/read.py TABLE STEPS` : digit counts, first appearances, opening blocks, tape at the rare wires.
- `tools/hand.py` : run a table from a hand-made tape.
- `tools/pavel.py` : Pavel's run as groups and units.
- `tools/t15_boot.py` : the opening of T written by hand.
