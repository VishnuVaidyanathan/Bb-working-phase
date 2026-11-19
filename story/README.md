# From a tape story to a table

The idea: do not write the table, and do not write the digits. Draw the tape at every
moment the head turns round (one picture per pass). Then ask which tables play those pictures.

| File | What it does |
|---|---|
| `story.c` | `story NSTATES file.story` : every table (up to renaming states) that plays all the pictures |
| `free.c` | the looser tool: `free NSTATES file` takes only the tape before and after each rule, and a limit on head turns, and invents the passes itself |
| `run.c` | `run TABLE [maxsteps]` : run a table from a blank tape |
| `passes.py` | cut a real machine's run into pass pictures (to test the tool, or to study a machine) |
| `cutfill.py` | the BB(5) story with other numbers, played on the tape alone, no table |
| `pics.py` | print a real machine's tape at every head turn, repeats folded |
| `twin.c` | run two tables side by side from a blank tape and report the first step where they differ |
| `tower3.py` | our own story "three blocks" as loose pictures |
| `nest3.py` | our own story with three counters and a deep borrow, as loose pictures |
| `marked.py`, `gate3.py` | the same stories with a lasting mark in every counter (an empty counter is a single 1) |
| `homes.py` | start a table on a tape of several counters and list each later rest position |
| `follow.py` | start a table on a three-block tape and list every later tape of that shape |
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

## Rediscovering the two 7-state champions from pictures

Pass pictures cut from the real run, no halt picture, 7 states:

| Machine | Pictures | Time | Tables found |
|---|---|---|---|
| Jeff Ketchersid's, first 200 steps | 46 | 0.4 s | 2 |
| Pavel Kropitz's, first 300 steps | 85 | 0.01 s | 2 |

Longer stories (1,500 and 1,300 steps) give the same two tables each.

In both cases one table is the champion with its halt entry left open, and the other is a twin:
the same tape and head for 3 billion steps (tested with `twin.c`), but no halt.

- Pavel's twin `1RB0LC_1LC1LF_1RD0LB_1RE1LA_1RB0RE_1RG1LD_0RG0RF` is his machine with the halt
  wire used as the start wire (states A and E change names, E0 becomes 1RB).
- Jeff's twin `1RB1LA_1RC0RF_0RD1RG_0LE0LD_0LA1LE_1LC0RG_1RC1RG` is his machine with the halt
  wire used as an ordinary wire: the champion's A0 then B1 becomes A0 then C1.

So the story without a halt picture leaves exactly one free choice: what the 14th wire does.

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

## The loose tool (`free.c`)

    S 0[0]0011000  S 0[0]1111110  1 30      before, after, at most 1 head turn, at most 30 steps

Test: 7 loose pictures of BB(5) and one halt picture (`examples/bb5_loose.txt`) give exactly the
champion's table, 5 states, in 0.15 seconds.

## Our own story: three blocks

Tape `1^a 0 1^b [0] 1^w`, head resting between the last two blocks.

- transfer: (a, b, w) -> (a, b-1, w+2)
- borrow:   (a, 0, w) -> (a-1, w+2, 0)
- tower:    (0, 0, w) -> the working block becomes the counter (several forms tried)

| Part | Result |
|---|---|
| transfer alone | fits in 3 states |
| transfer and borrow | fits in 5 states: 7 tables with 3 turns allowed (`examples/three_blocks_engine_5_states.txt`) |
| the same with w+3 | also fits in 5 states |
| transfer, borrow and tower | no table in 5, 6 or 7 states, for three forms of the tower rule (2 head turns allowed per picture) |

All 7 five-state tables follow the rules on a bigger tape than the pictures:
(2,2,1) -> (2,1,3) -> (2,0,5) -> (1,7,0) -> ... -> (1,0,14) -> (0,16,0) -> ... -> (0,0,32).
With both counters empty they run away to the left for ever, so by themselves they are not machines.

## Three counters with a deep borrow (`nest3.py`)

Tape `1^c3 0 1^c2 0 1^c1 [0] 1^w`. An empty counter is nothing: two 0s touch.

- transfer:    (.., c1, w)    -> (.., c1-1, w+2)
- borrow:      (.., c2, 0, w) -> (.., c2-1, w+2, 0)
- deep borrow: (c3, 0, 0, w)  -> (c3-1, w+3, 0, 0)   the working block becomes counter 2 and counter 1 keeps its place, empty

| Asked for | 5 states | 6 states | 7 states |
|---|---|---|---|
| transfer, borrow, deep borrow (w+2) | none | none | 10 tables |
| the same with w+3 | | | 4 tables |
| the same and a halt when all three counters are empty | none | none | none |

The tables are in `examples/three_counters_engine_7_states_*.txt`. Tested on a bigger tape, e.g.
`1LB1LA_1LE0RC_1RD1RC_0LA1RG_0LB0RF_0RD1RF_0RA1RG` from (2,0,0,0 | 1):
(1,1,3,0) -> (1,1,2,2) -> (1,1,1,6) -> (1,1,0,14) -> (1,0,31,0) -> (1,0,30,2) -> (1,0,29,6) -> ... -> (1,0,21,2046) ...
So counter 1 doubles for each unit of counter 2, and counter 2 is reloaded with the big block: three levels.

Limits found:
- these engines use all 14 wires, so there is no wire left for a halt, and none was found;
- with every counter empty they run away to the left for ever, also from a blank tape, so they are engines, not machines;
- a fourth counter only adds 1 to the third each time it pays, and five or more empty counters in a row collapse.

## Counters with a lasting mark (`marked.py`, `gate3.py`)

A counter of size c is c+1 cells of 1, so an empty counter is still a single 1 and the head can tell
"all counters empty" from "end of the tape".

| Asked for | Result |
|---|---|
| transfer and borrow | 5 states, 2 tables |
| transfer, borrow, and a halt when both counters are empty | 6 states, 1 table: `1LA1LB_1LE1RC_0RD0RC_0LA1RF_1RZ0LB_0RD1RF` |
| transfer, borrow, deep borrow (three marked counters) | no table in 5, 6 or 7 states |
| two counters and a tower when the working block is 0 mod 3 | no table in 5 or 6 states |

The 6-state table, started on counter 2 = c, counter 1 empty, working block empty, halts with 2^(c+2) + 1 ones:
c = 1: 39 steps, 9 ones; c = 3: 681 steps, 33 ones; c = 6: 43,692 steps, 257 ones.
It is a halting engine made from a story. It is not a machine: from a blank tape it runs away, and adding one
start state in all 784 ways gives nothing longer than 9 steps.
