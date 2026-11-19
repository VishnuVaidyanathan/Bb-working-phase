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
