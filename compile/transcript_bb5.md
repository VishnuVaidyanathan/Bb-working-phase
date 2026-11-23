# Story → transcript → TNF, done by hand for BB5 (Vishnu, 23 Nov)

Vishnu's hand sheet. Wires are numbered 0–9 (A0=0, A1=1, B0=2, B1=3, C0=4,
C1=5, D0=6, D1=7, E0=8, E1=9).

Story: two pairs (02 and 46), a three-word oscillator (159), two fillers
(3 and 7). The two pairs walk in opposite directions. The two fillers walk
in opposite directions. Start from a blank tape. Mod gate 3.

Transcript idea: `02, 46, 159` then `0 2 4 7777 6`, `0 33333 2`,
`46 159 159 159`.

Transcript → table:
- 0→2→4→6→0 gives the next states: A0→B, B0→C, C0→D, D0→A.
- A0 `1RB`, B0 `1RC`, B1 `1RB` (filler right), C0 `1RD`, D0 `1LA`,
  D1 `1LD` (filler left), E0 halt.
- Oscillator 1→5→9→1: A1→C, C1→E, E1→A. All three move L, because they
  must grow the counter on the left. Between them they write two 0s and one 1.

That leaves 3 tables (where the single 1 goes). Tested from a blank tape:

| the 1 is written by | table | result |
|---|---|---|
| A1 | `1RB1LC_1RC1RB_1RD0LE_1LA1LD_1RZ0LA` | halts after 47,176,870 steps with 4,098 ones |
| C1 | `1RB0LC_1RC1RB_1RD1LE_1LA1LD_1RZ0LA` | does not halt in 2,000,000,000 steps (runs off a 40-million-cell tape) |
| E1 | `1RB0LC_1RC1RB_1RD0LE_1LA1LD_1RZ1LA` | same |

The first is the BB5 champion of Marxen & Buntrock, reached from the story
with three tables to try.

Lesson for the method: the middle step is the **transcript** — the order in
which wires fire, written as words (pairs, oscillator) and fillers. Each
neighbour pair in the transcript fixes a "next state"; where the next cell
lies fixes L/R; the counts fix the writes.
