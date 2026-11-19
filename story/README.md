# From a tape story to a table

The idea: do not write the table, and do not write the digits. Draw the tape at every
moment the head turns round (one picture per pass). Then ask which tables play those pictures.

| File | What it does |
|---|---|
| `story.c` | `story NSTATES file.story` : every table (up to renaming states) that plays all the pictures |
| `run.c` | `run TABLE [maxsteps]` : run a table from a blank tape |
| `passes.py` | cut a real machine's run into pass pictures (to test the tool, or to study a machine) |
| `cutfill.py` | the BB(5) story with other numbers, played on the tape alone, no table |
| `cut3.py` | the same story as arithmetic, to see when it halts before any table exists |

Build: `gcc -O2 -o story story.c` and `gcc -O2 -o run run.c`.

## A picture

    S [0]0011 -> W 111[1]1 3

In state S on this tape (head on the bracketed cell), within 3 steps the machine stands in
state W on the second tape. S and W are only names; the search decides which real state each is.
`-> HALT 40` asks for a halt within 40 steps.

## The story of the BB(5) champion (Marxen and Buntrock)

- **cut**: going left, every 3 cells of the block keep one 1. The block becomes pieces `001`.
- **fill**: one sweep fills one piece and adds 2 cells on the left. 3 cells in, 5 out.
- **wall**: when no piece is left the head finds a 0, writes a 1 and starts cutting.
- **gate**: what is left over after cutting by 3: nothing = go on, one cell = go on with a longer start, two cells = halt.

## Results (all tested by running, nothing proved)

| Story | Fate by arithmetic, before any table | States | Tables found | Run from a blank tape |
|---|---|---|---|---|
| cut 3, fill adds 2 | halts in layer 15, about 47 million steps | 5 | 1 | `1RB1LC_1RC1RB_1RD0LE_1LA1LD_1RZ0LA`, halts at 47,176,870 with 4,098 ones: the champion |
| cut 3, fill adds 3 | halts in layer 3, about 200 steps | 6 | 2 | both halt at 183 steps, 11 ones |
| cut 3, fill adds 5 | halts in layer 11, about 1.6 billion steps | 7 | 0 | needs 8 states |

`examples/bb5_from_real_run.story` is 14 pictures cut from the real run; the tool finds the
champion's table from them in about 0.02 seconds.

## What this shows

- A tape story fixes the table. 40 pictures and one halt picture leave exactly one 5-state table.
- The fate of a story can be worked out on paper before a table exists, and the table then agrees.
- In this family every extra cell in the fill costs one state. Cut 3, fill 2 is the best it gives
  in 7 states or fewer. Bigger machines must reuse passes (nesting), not widen the fill.

## Limits

- Pictures must be one pass each. Longer pictures make the search very slow
  (the same BB(5) story as 7 long pictures did not finish in 5 minutes).
- A short story can be played by tables that leave the story later. Use enough pictures to
  cover every road, and always check the result from a blank tape.
