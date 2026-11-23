# Jeff Ketchersid's champion as a transcript (23 Nov) — observed, real run from a blank tape (`transcript_jeff.py`)

Table: `1RB0RG_1RC1RB_0RD1RZ_0LE0LD_0LF1LE_1RA1LF_1LC0RB`
Digits: A0=0 A1=1 B0=2 B1=3 C0=4 C1=5 D0=6 D1=7 E0=8 E1=9 F0=a F1=b G0=c G1=d.

| digit | wire | what it does |
|---|---|---|
| 0 | A0 `1RB` | home: give a cell, go right |
| 1 | A1 `0RG` | door: home found a 1 instead of a 0 |
| 2 | B0 `1RC` | end of filler 3: give a cell |
| 3 | B1 `1RB` | filler, walks right |
| 4 | C0 `0RD` | step over an empty cell |
| 5 | C1 `1RZ` | halt |
| 6 | D0 `0LE` | turn left |
| 7 | D1 `0LD` | take a cell, step left |
| 8 | E0 `0LF` | end of filler 9: step left |
| 9 | E1 `1LE` | filler, walks left |
| a | F0 `1RA` | give a cell, go to home |
| b | F1 `1LF` | filler, walks left (second left walker) |
| c | G0 `1LC` | behind the door, on a 0 |
| d | G1 `0RB` | behind the door, on a 1: take a cell, walk right again |

## The words

Round (5; 1 2 1) → (8; 0 2 1):

    0  3x5  2 4  7 6  9x8  8 a

Short pass (a word used inside every other job):

    … 2 4  6 8  b…b  a 1 d  3…3 …

Payment, 1 empty level (8; 0 2 1) → (1; 13 0 1):

    0 3x8 2 4 | 6 8 bx11 a 1 d | 3x9 2 4 | 6 8 bx10 a 1 d | 3x8 2 4 7 6 9x9 8 a
    0 3x9 2 4 7 6 9x13 8 | b a 1 c | 4 7 6 9 8 a

Payment, 2 empty levels: the short pass four times, then `b a 1 c` twice.

New row (40; 0 0 1): the short pass again and again, the filler one shorter
each time (3x41, 3x40, 3x39 …). The block is counted down into the row.

Start, blank tape: `0 2 4 6 8 bx2 a 1 d 2 4 6 8 b a 1 c 4 7 6 9 8 b a 1 c 4 7 6 9 8 a`
— the same words on an empty tape. No digit is used only for the start.

## What the digits show (observed)

- The round is one line with two fillers (3 right, 9 left), three gives
  (0, 2, a) and one take (7).
- Everything else is the round's line with one change: after `4` comes `6`
  instead of `7` (D reads a 0, not a 1). That is the only signal.
- Then the word `6 8 b… a 1 d` repeats. Digit 1 (the door) fires because the
  walker b comes home one cell short, so home meets a 1.
- Number of repeats seen: 2 short passes and one `1 c` for 1 empty level;
  4 short passes and two `1 c` for 2 empty levels; many for a new row.
  The count is on the tape, never in a state.
- Digit 5 (the halt) is the partner of 4: C meets a 1 where it expects a 0.

## Vishnu's reading of the table (23 Nov) — checked against the table

- **The even digits make one closed loop:** A0→B, B0→C, C0→D, D0→E, E0→F,
  F0→A. Digits `0 2 4 6 8 a` and back to 0. Six states, all on the loop.
- **Three fillers, all odd halves of loop states:** 3 (B1), 9 (E1), b (F1).
  The end of each filler is its even partner, which is on the loop. So the
  loop digits are the pairs: every filler starts from the loop and ends back
  on the loop.
- **A1 is the only door, and the only way into G.** G is the only state
  behind the door. Both of G's wires go back to the loop (G0→C, G1→B).
- **D1 is the take.** It points to its own state (`0LD`), shaped like a
  filler, but in a round it fires once because the next cell is a 0.
- **C1 is the halt.**

So the whole table is: one even loop of six + three fillers + one take +
one door with one state behind it + the halt.

The same check on other machines (the even wires only):

| machine | even wires | closed loop from A? |
|---|---|---|
| BB5 champion (Marxen & Buntrock) | A→B→C→D→A, E0 halt | yes, 4 states |
| Jeff Ketchersid's BB7 champion | A→B→C→D→E→F→A | yes, 6 states |
| Pavel Kropitz's BB7 machine | A→B→C→D→A, E0 halt, F→G, G→G | yes, 4 states |
| our 7-state stack | A→B→C→F→A, D→C, E→D, G0 halt | yes, 4 states |
| our round+payment draft | A→B→C→C, D0 halt, E→F→G→A | **no** (broken at C0) |

On a blank tape every read is a 0, so the machine starts by walking the even
loop. That is why a closed even loop gives the start for free.
