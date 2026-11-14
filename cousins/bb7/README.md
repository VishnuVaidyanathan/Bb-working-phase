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

## Files

- `results/lower_cousins_bb7.txt` : `H steps ones table`, biggest first.
- `results/not_yet_decided.txt` : tables still to be sorted (layers and gate).
- `results/proved_never_halt.txt.gz` : `N n table`, proved with window size n.
- `src/roles7.c` : the search. `PRE=33 ./roles7 7 BGCBD?EDFEAFCB 1000 20000000` runs one piece.
- `src/ncps.c` : the never-halts prover. Checked: it proves none of the 1,950 halting machines.
- `src/longrun.c` : plain long run from a blank tape.
