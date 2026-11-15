# BB(7) cousins search (work in progress)

Same test as for BB(5), now on the claimed BB(7) champion
`1RB0RG_1RC1RB_0RD1RZ_0LE0LD_0LF1LE_1RA1LF_1LC0RB` (found by Jeff Ketchersid).

**Roles kept fixed** (next state of each wire): `BGCBD?EDFEAFCB`
- ring on 0: A0→B, B0→C, C0→D, D0→E, E0→F, F0→A
- fillers: B1→B, D1→D, E1→E, F1→F
- side state: A1→G, G0→C, G1→B
- C1 is free (it is the halt wire in the champion)

Everything else is free: what each wire writes and which way it moves. A wire is filled in only when the run
from a blank tape reaches it. First move is to the right.

## Result so far

| | count |
|---|---|
| lower cousins: halt within 300 million steps, at least 1,000 steps | 1,958 |
| still running at 20 million steps and not a plain bouncer | 54,354 |
| of these, proved to never halt (closed position set) | 46,127 |
| of the rest, halt between 20 and 300 million steps | 8 |
| not yet decided (still running at 300 million steps) | 8,219 |

- The champion is found by the search. It is in the "not yet decided" list, as it must be: the search runs
  each table only 20 million steps.
- Biggest lower cousin: 295,113,423 steps, 20,486 ones.
- Halting was checked by plain running up to 20 million steps for every table, and up to 300 million steps
  for the tables that were not proved to never halt. Above 300 million steps nothing is known yet.

## Simulator pass (Shawn Ligocki's Quick_Sim)

The 8,219 undecided tables were split by tape width at 300 million steps:
5,252 fast growers (width 5,000 or more) and 2,967 slow growers.
The fast growers were given to Quick_Sim from `sligocki/busy-beaver` (by Shawn Ligocki), 10 seconds each, flag `-r`.

| | count |
|---|---|
| halt (tool) | 11 |
| proved to run forever (tool) | 2,196 |
| no answer in 10 seconds | 3,045 |

Halting cousins found this way, biggest first:

| steps | ones | table | checked by plain run |
|---|---|---|---|
| about 9 x 10^112 | about 4 x 10^56 | `0RB0LG_1RC1RB_1RD0LF_1RE0RD_1RF1LE_1LA1LF_---0RB` | no, too big |
| about 1.9 x 10^61 | about 5.8 x 10^30 | `1RB1RG_0LC1LB_0RD1LF_1RE1RD_0RF1RE_1RA0LF_1RC---` | no, too big |
| about 1.7 x 10^45 | about 7.5 x 10^22 | `1RB1LG_1LC1LB_1RD0LE_1RE1RD_1LF0RE_1LA1LF_---0LB` | no, too big |
| 408,558,058,408,175,688 | 857,557,346 | `1RB0LG_1RC1RB_0LD1LE_0LE1LD_1LF0RE_1LA---_0RC1RB` | no, too big |
| 114,196,411,835,282,439 | 692,549,585 | `1RB1LG_1RC1RB_1RD0RF_1LE---_0LF1LE_1LA1RF_1LC0RB` | no, too big |
| 113,622,663,316,752,575 | 445,914,500 | `1RB1RG_0LC1LB_0RD1LF_1RE0RD_0RF1RE_1RA0LF_1RC---` | no, too big |
| 4,034,860,548,018,943 | 86,564,054 | `0RB0LG_1RC1RB_0LD1RE_0LE1LD_1LF0RE_1LA0RF_---0LB` | no, too big |
| 29,187,560,564 | 155,969 | `1RB0LG_1RC0RB_1RD1LE_1RE---_1LF1LE_1LA1RF_0LC1LB` | yes |
| 2,863,705,134 | 65,542 | `0RB0LG_1LC1RB_0LD0RC_1LE1LD_1RF---_1LA1LF_0LC1LB` | yes |
| 2,863,574,028 | 65,542 | `0RB0LG_1LC1RB_0LD0RC_1LE1LD_1LF---_1LA1LF_0LC1LB` | yes |
| 1,732,594,991 | 70,372 | `0RB0LG_1RC1RB_0RD0RB_1LE0LD_1LF1LE_1LA0LF_---0LB` | yes |

The seven rows marked "too big" rest on the tool alone for now. Each still needs our own layer rule and gate
written out and checked. None is bigger than the champion.

Second pass on the 3,045 with no answer (20 seconds, flags `-r --exp-linear-rules --exp-meta-linear-rules`),
stopped after 705 tables because it gave little: 0 halt, 6 run forever, 698 no answer, and 1 where the tool
stopped on a power tower more than 500 levels high. That one is a base-4 tower machine; it is proved in Coq
to never halt, see [`base4/`](base4/).

The 2,967 slow growers (10 seconds, flag `-r`): 0 halt, 748 run forever, 2,206 no answer, 13 tool crashes.

Still open: about 5,250 tables with no answer from the tool.

## Files

- `results/lower_cousins_bb7.txt` : `H steps ones table`, biggest first.
- `results/not_yet_decided.txt` : tables still to be sorted (layers and gate).
- `results/proved_never_halt.txt.gz` : `N n table`, proved with window size n.
- `src/roles7.c` : the search. `PRE=33 ./roles7 7 BGCBD?EDFEAFCB 1000 20000000` runs one piece.
- `src/ncps.c` : the never-halts prover. Checked: it proves none of the 1,950 halting machines.
- `src/longrun.c` : plain long run from a blank tape.
- `results/quick_sim_pass1.txt` : Quick_Sim answer for each of the 5,252 fast growers (HALT, INF or T = no answer).
- `results/halting_cousins_from_quick_sim.txt` : the 11 halting ones.
- `results/quick_sim_no_answer.txt` : the 3,045 with no answer yet.
- `results/quick_sim_slow_growers.txt` : Quick_Sim answer for each of the 2,967 slow growers.
- `results/quick_sim_pass2_partial.txt` : second pass, first 705 tables.
- `src/qs2.py` : batch runner for Quick_Sim.
