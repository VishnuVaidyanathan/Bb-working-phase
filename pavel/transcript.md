# Pavel Kropitz's BB7 machine as a transcript (23 Nov) — observed, real run from a blank tape (`transcript_pavel.py`)

Table: `1RB0RA_1LC1LF_1RD0LB_1RA1LE_1RZ0LC_1RG1LD_0RG0RF`
Digits: A0=0 A1=1 B0=2 B1=3 C0=4 C1=5 D0=6 D1=7 E0=8 E1=9 F0=a F1=b G0=c G1=d.

| digit | wire | what it does |
|---|---|---|
| 0 | A0 `1RB` | loop: give a cell, go right |
| 1 | A1 `0RA` | filler right that takes (points to itself) |
| 2 | B0 `1LC` | loop: give a cell, turn left |
| 3 | B1 `1LF` | step left into F |
| 4 | C0 `1RD` | loop: give a cell, go right |
| 5 | C1 `0LB` | take a cell, step left, back to B |
| 6 | D0 `1RA` | loop: give a cell, go right, back to A |
| 7 | D1 `1LE` | step left into E |
| 8 | E0 `1RZ` | halt |
| 9 | E1 `0LC` | take a cell, step left, back to the loop |
| a | F0 `1RG` | give a cell, go right |
| b | F1 `1LD` | step left, back to the loop |
| c | G0 `0RG` | filler right over empty cells (points to itself) |
| d | G1 `0RF` | take a cell, go right, back to F |

## Structure (checked against the table)

- **Even loop of four:** A0→B, B0→C, C0→D, D0→A. Digits `0 2 4 6`.
  All four give a cell. Moves R, L, R, R.
- **Two pair-fillers, walking opposite ways:**
  `2 5 2 5 …` (B0, C1) walks LEFT, two states pointing at each other;
  `a d a d …` (F0, G1) walks RIGHT, two states pointing at each other.
  Each reads 0 then 1 and writes 1 then 0: it shifts a 0 1 0 1 pattern by one.
- **Two single fillers, both to the right:** 1 (A1, takes) and c (G0, over
  empty cells).
- **Gate:** `4 7 9`, then 5 or 4. Its third way out is 8, the halt
  (E meets a 0).
- Off the loop: E (gate and halt), F and G (the right-walking pair).

## The transcript from a blank tape, cut at digit 0

    0 2 5 2 4 7 9 4 6 1
    0 3 b 6 1 1
    0 2 5 2 4 7 9 5 3 b 6 1 1
    0 2 5 2 4 7 9 5 2 4 7 9 4 6 1
    0 2 5 2 5 3 a d a d a d b 6 1
    0 3 b 6 1 1 1
    0 3 b 6 1 1
    0 2 5 2 4 7 9 5 2 4 7 9 5 3 b 6 1 1
    0 2 5 2 4 7 9 5 3 a d a c d a d b 6 1
    …
    0 2 5 2 4 7 9 5 2 5 2 5 2 5 2 5 3 a d a d a d a d a d a c d a d b 6 1

Two kinds of line: the short line `0 3 b 6 1…` and the long line
`0 2 5 … 3 … b 6 1`. Every line starts with 0 and ends `6 1…`.

How often each digit fired in 3,000,000 steps: 2 and 5 about 739,700 each;
a and d about 734,900 each; 1: 11,984; 0, 3, 6, b about 6,770 each;
4, 7, 9 about 3,350 each; c: 1,549; 8: never (the halt).
So the two pair-fillers do almost all the walking.
