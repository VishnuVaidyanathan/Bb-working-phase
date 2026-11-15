# The champion's opening and its parity gate (working notes, 15 Nov 2026)

Machine `1RB0RG_1RC1RB_0RD1RZ_0LE0LD_0LF1LE_1RA1LF_1LC0RB` (found by Jeff Ketchersid).
Everything here is tested by plain running on small hand-made tapes, unless it says "proved".

## The opening is a small copy of the big run

| step | tape (head at `[G0]`) | what it is |
|---|---|---|
| 141 | `(10)^7 [G0]` | the boot has laid 7 pairs of `10` on the left |
| 170 | `110 [G0] (1100)^2 1` | 3 pairs make the end-mark and the last 1, 4 pairs make 2 units |
| 319 | `10 [G0] 1^13 0000 1` | gate with P = 13 (one tripling 3*2+6 = 12, plus the stray 1 of the end-mark) |
| 3755 | `110 [G0] 1 (1100)^21 1` | the restart has turned 42 pairs into 21 units, with one extra 1 in front |
| 3954 | `10 [G0] 1^16 0000 (1100)^19 1` | block 3 -> 15, plus the stray 1 = 16; the proof `BB7Halts.v` starts here |

Generation 1: 2 units, block starts at 2 (even), ends 13 (odd): restart.
Generation 2: 19 units, block starts at 3 (odd, because of the extra 1), ends 16 (even): halt.

## The gate (a block that is a single 1)

| P | where the single 1 is | result |
|---|---|---|
| even | anywhere | halt |
| odd | in the middle of the tape | halt |
| odd | the last cell of the tape | restart with (3P - 1)/2 units, new block 14 (gap 2) or 16 (gap 4) |

Tested: restart for P = 13, 15, 17, 19, 21, 25, 31 gives 19, 22, 25, 28, 31, 37, 46 units.
Proved (`units_halt`): every restarted tape with 1 to 197 units halts.

## Parity book-keeping

- Tripling (gap 2): P -> 3P + 6. Parity of P is kept.
- Wider gap (2j, j >= 2): the old block becomes a counter of 3P + 8 - 2j (same parity as P); the new block is 2.
- A counter loses 2 per tripling. An even counter reaches 0 and two gaps join. An odd counter reaches 1,
  and that is a gate in the middle of the tape: halt.

So an odd number anywhere ends the run, except an odd P that reaches the last cell by triplings only.
Example (hand-made tape): `1^7 00 1^6 00 1` gives P = 27, 85, 267 and then a restart with 400 units.

## What this means for a bigger machine

The level of the run is the number of units, and that is set by P at the first gate.
The champion's own table would halt at a much higher level from a larger odd P; from a blank tape it gets 13,
because the boot lays 7 pairs. A bigger machine of this kind is a cousin whose boot gives a larger odd P at
the last cell.
