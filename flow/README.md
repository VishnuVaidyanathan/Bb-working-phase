# Wiring first: the recipe in digits

Vishnu's recipe for a deep machine, written in digits:

1. start with `0 2` (a blank tape)
2. one word of three digits that always stick together (`479` in Pavel Kropitz's machine, `159` in the BB(5) champion)
3. about 9 digits that branch (go to two digits)
4. about 9 roads used equally often (the river)
5. fillers (loops) that grow with the depth

| File | What it does |
|---|---|
| `flow.c` | `flow WIRING STEPS`: the wiring is fixed (which state each of the 14 digits flows to); every choice of write and move is tried from a blank tape, as far as the run needs it; prints each table still alive and its road counts |
| `recipe.py` | `recipe.py WIRING file`: keeps the tables whose road counts fit the recipe |
| `wirings.py` | random wirings that obey the fixed part of the recipe |
| `nest.py` | `nest.py TABLE [STEPS]`: the nest of the filler: the lengths of its runs in order, and how many times "climb, fall back, and look at the tops" can be repeated |
| `digits.py` | `digits.py TABLE [SHOW [STEPS]]`: any table shown in digits: first digits folded, what comes before and after every digit, the filler and the tops of its nest |
| `nestc.c` | the nest test and a tape-growth test as a fast filter over a list of tables |
| `riverc.c` | fast test: size of the river (roads used equally often), and the number of idle digits |
| `ranges.py` | group a machine's roads into ranges of equal use |
| `batch.sh` | runs the two tools over a list of wirings |

Wiring = 14 letters, the next state for digits 0..d, Z for the halt. Jeff Ketchersid's is `BGCBDZEDFEAFCB`, Pavel Kropitz's is `BACFDBAEZCGDGF`.

## "Fillers grow with the depth" as a number

Filler uses per river round, at the end of the run divided by the same at a quarter of the run.
A plain back-and-forth machine gives exactly 2. Jeff's machine gives 2.28, Pavel's 2.77. The recipe asks for 2.15 or more.

## Results (tested, 200,000 steps per table)

| Wiring | Tables alive | Fit the recipe | What they are (Shawn Ligocki's Quick_Sim) |
|---|---|---|---|
| Pavel's | 29,152 | 2 | Pavel's own machine, and one proved to run for ever (2 rule levels) |
| Jeff's | 10,808 | 9 | 8 proved to run for ever with 2 levels, 1 no answer; Jeff's own table does not pass at this run length |
| 60 random wirings | 426,282 | 115 | of the first 60 checked: 28 proved to run for ever (20 with 2 levels), 24 no answer in 15 s with 1 level, 8 other; no halter, nothing above 2 levels |

So the recipe keeps about 1 table in 3,700 and what it keeps has nested structure, but no new deep halting machine has come from it yet.

## "The filler must have its own nest" (`nest.py`)

Take the most used loop and list the length of each of its runs, in order.

- depth 1, a plain grid: the lengths only climb
- depth 2: they climb and fall back (a saw), and the tops of the teeth only climb
- depth 3: the tops themselves climb and fall back; and so on

Measured over 4,000,000 steps from a blank tape:

| Machine | Nest depth |
|---|---|
| a plain back-and-forth machine | 1 |
| BB(5) champion | 2 |
| Pavel Kropitz's 6-state tower, the BB(6) champion, Andrew Ducharme's 4-arrow machine | 2 (their deeper nests do not show this early) |
| Pavel Kropitz's 7-state machine | 3 |
| Jeff Ketchersid's machine | 3 |

Of the 126 tables that fitted the recipe (`fits_nest_depth.txt`, 1,500,000 steps): depth 1: 3, depth 2: 100, depth 3: 16, depth 5: 7.
The 23 with depth 3 or more are Pavel's machine and 22 others: 7 proved to run for ever, 6 that keep a tiny tape
(counters: a nest with no growth), and 9 growing with one rule level and no answer yet. No new deep halter.
So the nest test must be used together with growth of the tape.

## Every live table checked (60 wirings, 426,282 live tables)

| Test | Tables left |
|---|---|
| filler has a nest of depth 3 or more, and the tape grows | 5,039 (from 38 of the wirings) |
| and a river of at least 9 roads in one range | 967 |
| and at most 3 idle digits | 887 |

`nest_pass_60_wirings_river.txt` lists the 5,039 with river size, river count, idle digits and digits used (2,000,000 steps).
By these tests Jeff Ketchersid's table has a river of 9 and 1 idle digit; Pavel Kropitz's has a river of 7, so it fails the "river of 9" line.
