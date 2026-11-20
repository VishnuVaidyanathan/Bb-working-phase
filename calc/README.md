# calc : remainders of numbers too big to write

`remainder.py` takes a number written as a formula (whole numbers, + - *, exact division, powers, and
"this rule repeated N times from X", written `(λg → RULE)^(N) (X)`) and gives its exact remainder on division by m.
Self test: `python3 remainder.py --test` (842 checks: against plain computing, against a closed form, and N steps = one step after N-1).

`quick_sim_with_remainders.py` runs Shawn Ligocki's Quick_Sim (not included; set `QUICK_SIM_DIR`) and supplies the remainder
at the point where it stops with "Cannot mod Iterated_Math". `REMAINDER_LOG=file` records every remainder asked.

`check_twice.py LOG` redoes every logged remainder by a second route.

## Results (8-state stack `1LH1RG_1RC1RB_0LF0LD_0LF1LD_0LD0RB_0RA1LF_1RZ1RE_1RB---`, started with a first block written by start-up states)

| first block | result (tested: Quick_Sim + one remainder mod 2, checked twice) | ones |
|---|---|---|
| 1 | halts | 12 |
| 3 | halts | 96 |
| 5 | halts | about 10↑↑3 |
| 7 | halts | between 10↑↑10↑↑10↑↑3 and 10↑↑10↑↑10↑↑4 |
| 9 | halts | between 10↑↑↑10↑↑↑10↑↑10↑↑10↑↑3 and 10↑↑↑10↑↑↑10↑↑10↑↑10↑↑4 |

These are not blank-tape machines (13 to 17 states with the start-up part). Not checked by a second simulator.
