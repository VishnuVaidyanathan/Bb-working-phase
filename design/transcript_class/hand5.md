# Can a row form in the loop-of-five type? Hand analysis (23 Nov) — worked on paper, then each step tested with `compile/tape2.py`

Type: even loop A0→B0→C0→D0→E0→A; three fillers, one take, one door on the
odd halves; F behind the door (one wire back, one on to G); G = gate (one
free wire, one halt). Tape: solid runs, two empty cells between them.

## 1. A round fits in one lap of five — tested

    0  3…  2 4  7 6  9…  8        (5; 6) → (8; 5)

| digit | wire | job |
|---|---|---|
| 0 | A0 `1RB` | home: give a cell, go right |
| 3 | B1 `1RB` | filler right over the block |
| 2 | B0 `1RC` | first gap cell: give |
| 4 | C0 `0RD` | second gap cell: step over |
| 7 | D1 `0LD` | take one cell of the store, step back |
| 6 | D0 `0LE` | turn left |
| 9 | E1 `1LE` | filler left over the block |
| 8 | E0 `1LA` | left end: give, step left; A then reads a blank: home |

Give 3, take 1. It is Jeff Ketchersid's lap without the sixth loop digit.

## 2. "Store empty" opens the door by itself — tested

When the store is empty the take (7) is missing, so the loop is one digit
ahead: `… 2 4 6 8 1`. E0 fires at the front instead of at the left end, and
A lands on a 1: the door (digit 1, A1). No wire is spent on noticing.

## 3. A landing fits behind the door, with G as the gate — tested

| digit | wire | job |
|---|---|---|
| 1 | A1 `1LF` | door, at the front: start walking home |
| b | F1 `1LF` | F's "back" wire: filler left over the old block |
| a | F0 `0LG` | at the left end: leave an empty cell, go on to G |
| c | G0 `0LA` | leave a second empty cell; A then reads a blank: home, a new block starts |
| – | G1 | **halt**: fires only if G finds a 1 two cells left of the block |

Table: `1RB1LF_1RC1RB_0RD---_0LE0LD_1LA1LE_0LG1LF_0LA1RZ` (C1 is spare).
Hand tape: (11; empty; 2; 3) → `… 2 4 6 8 1 bx12 a c` → (3; 13; 2; 3).
**From a blank tape it starts itself:** `0 2 4 6 8 1 b a c` → block 3, then
3 → 12 → 39 → … (b → 3b + 3). G is entered once per landing (6 times in
2,000,000 steps, last at step 449,488).

## 4. But the row is never used

In this hand machine a landing costs nothing. Every time the front store
runs out, the block lands and a new block triples it again. The stores
further right (the 2 and the 3 above) are never reached. A row can sit on
the tape, but it does no work, and the machine triples for ever.

For a row to work, two more jobs are needed:
- **pay**: a landing must take something from the next store, so the number
  of landings is counted by that store (this is what makes one arrow per
  store);
- **lay**: something must lay a new row when the stores are gone.

This arrangement has one spare wire (C1) for two jobs. So in this exact
arrangement a working row does not fit. Other arrangements of the same type
may share jobs the way Jeff's short pass does (one word repeated, the count
kept on the tape). Not proved impossible; the Quick_Sim screening of the
class is the test.

## 5. Where the halt would come from

G halts when it finds a 1 two cells left of the block. That is exactly the
place for a small left counter: each landing would have to move toward it or
use one cell of it. In this machine the left side is always blank, so the
halt never fires.

## 6. Vishnu: "What if the halt is outside — can pay and lay be built within those two states?"

Halt moved to C1 (C expects an empty gap cell and meets a 1 — a collision).
Then F and G have four working wires, plus the door: five wires behind the
round. Count check: Jeff Ketchersid's table spends the same five on these
jobs (door A1, second left walker F1, the give F0, and G0, G1). So by count
it is possible.

By hand so far (tested): a **pay** trip fits —
A1 `1RF`, F1 `1RF`, F0 `1RG`, G0 `0RD`, then the round's own take and walk
home: `… 2 4 6 8 1 b a c 7 6 9… 8`.  (11; empty; 4; 3) → (16; 3; 3): the
next store pays 1 and becomes the front store. But this returns home as a
plain round, so nothing lands, and only G1 is left. By hand I have pay
(4 wires) or land (4 wires), not both in 5.

So the question goes to a search inside the hand frame (frame5.py):
fixed = the hand round (A0, B0, B1, C0, D0, D1, E0, E1) and the halt on C1;
open = the door A1 and all four wires of F and G. 2,458,624 tables.
