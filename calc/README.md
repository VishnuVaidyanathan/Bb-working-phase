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

## Gate study (20 Nov) - arithmetic only, no tables

Model: round adds K, fresh store m, leftover RH halts (stackcalc.py). Checked against the real 8-state stack for K=3, m=2 only;
for other K, m it is the same rules with other numbers, not yet a table.

* A row of n stores ends with about n-2 arrows.
* Stores of 2: every long row ends with the same leftover, so the machine halts at its first row (or never). Arrows = first row - 2.
* Stores of 3 with round +4 or +5: the leftover at the end of a long row alternates with the row length (observed for n = 1..16).
  A first block of 2 to 5 cells makes a first row of 2 stores, survives it, and halts at the end of the second row:
  K=4, RH=0, first block 3: rows 2, 23 (21 arrows);  K=4, RH=1, first block 4: rows 2, 92;  K=4, RH=2, first block 5: rows 2, 370;
  K=5, RH=0, first block 3: rows 2, 177;  K=5, RH=2, first block 2: rows 2, 35;  first block 4: rows 2, 885.
  Some first blocks (7 to 12) halt at the end of a tower-sized row.
Full lists: gatescan_blank_K11_m7.txt, cheap_gates_by_first_block.txt.

## A third stopping place in the simulator, fixed (21 Nov)

33 of Polygon's 711 holdouts stopped in Quick_Sim with "'ExpTerm' object has no attribute 'min_value'" (not a remainder problem).
Cause: inside a formula that still has a variable, a power term that is a plain number has no "smallest value" and no variable list recorded.
`quick_sim_with_remainders.py` now supplies them when asked (the smallest value of a plain number is itself; it has no variables).
Nothing in Shawn Ligocki's code is changed on disk. First table tried went from stuck at 3 arrows to about 6 arrows in 90 seconds.
