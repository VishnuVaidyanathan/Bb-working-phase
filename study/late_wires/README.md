# Late wires freed (working notes, 15 Nov 2026)

Question: keep the opening of a known deep machine and let the last wires to appear be anything.
Does another deep machine come out?

Family 1: each of 21 known 7-state machines (`../machines.txt`), with the last two wires to appear in its run
set to every write, move and next state. 16,443 tables.

| step | tables |
|---|---|
| halt in a plain run of 5 million steps | 6,057 |
| proved to run forever (closed position set) | 9,810 |
| given to Quick_Sim (8 seconds; 26 of them 150 seconds) | 576 |
| Quick_Sim: run forever | 326 |
| Quick_Sim: halt | 8 |
| Quick_Sim: stopped at a power tower more than 500 high | about 21 |
| Quick_Sim: no answer | about 220 |

Halting tables found (none has more than 2 rule levels):

| size | table | opening of |
|---|---|---|
| 10↑↑140 | `1RB0LC_1LC0LD_1LA1LB_1LG1RE_1LD0RF_0RA1RE_---0RC` | T140 |
| 10↑↑140 | `1RB0LC_1LC0LD_1LA1LB_1LG1RE_1LD0RF_0RA1RE_---1LC` | T140 |
| a power tower 8 high | `1RB0LC_1LC0LD_1LA1LB_1LG1RE_1LD0RF_0RA1RE_---1LE` | T140 |
| about 10^899 | `1RB0LC_1LC0LD_1LA1LB_0LG1RE_1LD0RF_0RA1RE_---0LE` | T140 |
| about 3 x 10^19 | `1RB0RG_1RC0RF_1LD---_1LF0LE_1RA1LD_1LG1RE_0LB0LA` | T46 |
| 44,471 / 4,178 / 4,096 | three small ones | T140, T93, T22 |

The two at 10↑↑140 are the same size as their seed and are most likely the same machine with one wire written differently.

No table with 3 or more rule levels came out. The undecided ones are mostly towers.

`family1_quick_sim.txt` has every Quick_Sim answer. Scripts: `gen.py`, `pipe.sh`, `qs3.py`.
