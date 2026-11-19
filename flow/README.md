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
| `zonec.c` | fast test: the zones of a machine (small roads, river, next zone, fillers) and the growth number |
| `batch3.sh` | the whole chain over a list of wirings: flow, nest test, zone test |
| `gatec.c` | fast test: does the halt hang off a counting loop (like 159 or 91), how many ways the run has left that loop, and the longest row of pieces 01 or 001 on the tape |
| `neighbours.py` | every table one wire away from a table, including every other place for the halt |
| `haltalive.py` | a check on the table alone: can the halt ever read the symbol it needs? |
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

### The 887 in Shawn Ligocki's Quick_Sim (8 seconds each, `river9_887_quick_sim.txt`)

| Result | Tables |
|---|---|
| proved to run for ever | 526 (163 with no rule level, 329 with one, 34 with two) |
| no answer, no rule found | 251 |
| no answer, one rule level | 106 |
| other | 4 |
| halts | 0 |
| three or more rule levels | 0 |

The top unanswered table by nest depth and river size is `1RB0LD_1LD0LB_0RF1LB_1RA1LC_0LD0RE_1RZ0LG_1RG1RE`:
a river of 15 roads all used 17,460 to 17,462 times in 2,000,000 steps, a second range at exactly double (34,921),
a third near four times (68,724), and a nest of depth 9 whose tops double at each level.
It does not halt in 20,000,000,000 steps and has only 201,450 ones by then.
So it is a counter: a perfect nest and ranges in powers of two, but slow growth.

## The zone rule (Vishnu, 19 November)

"A few must be small, then the river must have 7 to 9, then 1 or 2 in the next zone, then definitely 2 must be exponential."

`zonec.c` counts roads in each zone and the growth number (filler per river round at the end of the run, divided by the
same at a quarter of the run). At 4,000,000 steps:

| Machine | small | river | next | fillers | growth |
|---|---|---|---|---|---|
| Jeff Ketchersid's | 11 | 9 | 1 | 2 | 2.31 |
| Pavel Kropitz's 7-state | 6 | 6 | 6 | 2 | 2.17 |
| Andrew Ducharme's 4-arrow | 7 | 6 | 9 | 1 | 2.11 |
| BB(5) champion | 5 | 6 | 3 | 2 | 2.06 |
| a plain back-and-forth machine | | | | | 2.00 |
| the counter `1RB0LD_1LD0LB_0RF1LB_1RA1LC_0LD0RE_1RZ0LG_1RG1RE` | 2 | 15 | 3 | 2 | 1.39 |

The growth number puts the known machines in the order of their depth, and puts the counter below 2.

Rule as tested: small >= 1, river 7 to 9, next 1 or 2, fillers = 2, growth >= 2.15.

| Where | Nested tables | Fit the zone rule |
|---|---|---|
| Jeff's and Pavel's wirings (39,960 live tables) | 444 | 1: Jeff's own table |
| 60 random wirings (426,282 live tables) | 5,039 | 1: `1RB0LE_1LE1LD_1RZ0RG_0RF1LB_1RC1LA_0LA0LB_1RD1RG`, proved by Quick_Sim to run for ever (2 rule levels) |

`nest_pass_60_wirings_zones.txt` has the zone line of each of the 5,039.

### Can the one fitting table be changed into a halter?

`1RB0LE_1LE1LD_1RZ0RG_0RF1LB_1RC1LA_0LA0LB_1RD1RG`. Its halt is digit 4 (C reads 0), and the only way there is the word `1 8 4`:
the loop `(91)` eats 1s two at a time going left, and ends either `9 0` (go on) or `1 8 4` (halt). So it is a parity gate.
In the run it has always ended `9 0`, and Quick_Sim proves it always will.

| Change | Tables | Halt (all within 4,000 steps) | Nested and growing like a deep machine | Of those, proved to run for ever |
|---|---|---|---|---|
| one wire (including moving the halt) | 715 | 500 | 2 | 2 |
| two wires | 147,906 | not counted | 19 | 19 |

So within two wire changes there is no deep halter. (Tested, 2 rule levels each.)

## Arithmetic gate and pieces (Vishnu, 19 November)

"It must be arithmetic, the gate. And the 001 or 01 must be there, and it must fall after climbing a few good layers."

`gatec.c` on known machines (2,000,000 steps): BB(5): loop of 3, two safe exits, halt 1 step away, 478 pieces `001`.
Pavel Kropitz's: loop of 2, halt 3 steps away, 1,044 pieces `01`. Jeff Ketchersid's: no such loop and no such pieces (his units are `1100`).

Of the 5,039 nested tables from the 60 wirings: 581 have a counting loop within 2 steps of the halt and pieces on the tape;
5 of those also have fillers growing faster than a plain machine. In Quick_Sim (60 s):

| Table | Result |
|---|---|
| `1RB1LE_1LE1LD_1RZ1LG_1RF0LB_1RC1LA_1RA1RB_0RD1RG` | **reaches a tape of `(10)^N` with N a power tower of 10s about 500 high in 1.2 seconds, then the tool stops ("Too many layers of ExpInt: 501"). No halt seen. 2 rule levels, 2 Collatz rules.** With the tool's limit raised it goes on for about five times as many rule applications and then runs out of recursion depth, still without a halt. |
| `1RB---_0LC0LF_1LE0RD_1RC1LG_1RG1LC_1RZ1RA_0LD1RB` | no answer, 1 level, size beyond 10^60 |
| `1RB1RE_1RE1RD_1RZ1LG_0RF1RB_0LC0RA_1RA1LB_1LD1LG` | no answer, 1 level, size about 10^89,371 |
| `1RB1LE_0RD1RC_0RG0RB_1LA0LA_1RF1LA_1RZ0LE_0LD0RB` | no answer, no rule found |
| `1RB0LE_1LE1LD_1RZ0RG_0RF1LB_1RC1LA_0LA0LB_1RD1RG` | proved to run for ever |

The first one is a tower machine (each round the stripe count N becomes about 10^N). It climbs, but has not been seen to fall.
Its wiring is `BEEDZGFBCAABDG`, the same wiring as the parity-gate table above.

### 150 more wirings (seed 2)

7,043 nested tables. Zone rule: 0 fit. Arithmetic gate, pieces and growing fillers: 26 (`gate_fits_150_wirings_quick_sim.txt`).
In Quick_Sim (30 s): 11 proved to run for ever, 14 no answer (6 with no rule found, 8 with one level), 1 where the tool failed.
No halter and no tower. The three with the highest growth number (about 3.0) do not halt in 30,000,000,000 steps and
have fewer than 200,000 ones by then, so they grow slowly.

### Cousins and neighbours of the tower machine

Cousins: all 322 nested tables with the wiring `BEEDZGFBCAABDG` in Quick_Sim (15 s, `tower_wiring_family_322_quick_sim.txt`):
184 proved to run for ever, 134 no answer, 4 where the tool stopped (one of them the tower machine). No halter, no second tower.

Neighbours: the tower machine `1RB1LE_1LE1LD_1RZ1LG_1RF0LB_1RC1LA_1RA1RB_0RD1RG` and the slow table
`1RB0LD_1LF0RE_1LC1LG_1LA1RB_1RC0RD_1RZ1LG_0LD1RB`, every one-wire change including every other place for the halt: 1,320 tables.
766 halt within 74 steps. Of the 554 others, 18 are nested (`tower_and_slow_neighbours_nested_quick_sim.txt`).

Changing only the wire F1 of the tower machine (1RB in the original):

| F1 | Result |
|---|---|
| 1RB (original) | tower about 500 high, tool stops, no halt seen |
| 1LA | tower about 500 high, tool stops, no halt seen |
| 1LF | proved to run for ever, with a rule of level 3 |
| 0LC, 0LD | no answer, one level, about 10^12,500 |
| 0RE | no answer, no rule found |
| 0LA, 1LG, 1RE | proved to run for ever |

Moving the halt to any other wire gives a machine that halts within 74 steps or loses the nest.

The other 536 neighbours (not nested, no quick halt) in Quick_Sim (8 s, `tower_and_slow_neighbours_rest_quick_sim.txt`):
528 proved to run for ever, 4 no answer, 4 where the tool stopped. Two of the last four reach exactly the same tower as the
tower machine (`...1RF0LB_1RG1LA...` and `...1RZ1RG...`): the same run with a wire changed that does not matter. No halter.

## Can the halt be hit at all? (`haltalive.py`, Vishnu, 19 November)

"The halt must hit a zero. Is that one digit enough?"

In the tower machine `1RB1LE_1LE1LD_1RZ1LG_1RF0LB_1RC1LA_1RA1RB_0RD1RG` the halt is C reading 0. C is entered only by
E0 (write 1, move right). E is entered only by A1 and B0, and both write 1 and move left. So E0 always steps back onto a
cell that has just been written 1, and C reads 1 every time. **The halt can never be hit: this machine never halts.**
This is a proof from the table alone (two steps), and it settles the tower machine and its second-tower neighbour.

The same check on other machines: Jeff Ketchersid's, Pavel Kropitz's and BB(5) are alive (the halt reads a fresh cell);
the parity-gate table is alive (A1 writes 0 and E0 steps back onto it); the slow table is dead.

Of the nested tables: 2,099 of 5,039 (60 wirings) and 3,099 of 7,043 (150 wirings) have a dead halt by this check.
So "the halt is alive" is now a line of the recipe, and it should be applied first because it costs nothing.
