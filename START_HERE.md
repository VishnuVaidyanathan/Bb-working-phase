# Start here (state on 15 Nov 2026, evening)

The idea: we do not design the table, we design the transcript. One digit per step, `2*state + symbol read`.

## What is established

1. The boot is the machine at small size. Written by hand and matched: `bb7/boot/boot_by_hand.py` (319 digits), `study/tools/t15_boot.py` (570 digits).
2. A written transcript fixes the table: `bb7/transcript_to_table/` (`sketch.py`, `draft.py`, `prefix.py`).
3. The gate is the counter modulo its own step: `study/README.md`.
4. Above three levels the levels are on the tape; in the 4-arrow machine each group adds two arrows: `study/d1_four_arrows.md`.
5. Wires share jobs; the gate is a rare job of a common wire: `study/wire_jobs.md`.

## What did not work

Writing from known words gives back the same machine. Keeping a deep opening and changing the tail
(about 82,000 tables, `study/late_wires/`) gives no new deep machine. Deep machines have no deep neighbours.

## Open threads

- Pavel Kropitz's 7-state machine: how 5 becomes 14 units (its depth word), and its halting gate (mod 3 expected).
- Why two arrows per group in the 4-arrow machine.
- The pen-and-paper method: tape story, passes, digits; wires as a budget; the map of junctions.

## Tools that need rebuilding in a fresh workspace

- Shawn Ligocki's Quick_Sim: clone `sligocki/busy-beaver`, `pip install gmpy2 psutil`, then
  `export QUICK_SIM_DIR=/path/to/busy-beaver/Code`. The scripts in `study/tools/` read that setting.
- `cousins/bb7/src/`: `longrun.c`, `ncps.c`, `roles7.c` (compile each with `gcc -O2`).
- Everything else is plain Python 3. `study/tools/README.md` lists every script.

## Standing rules

Credit Jeff Ketchersid (champion), mxdys (BB(6) rules), Shawn Ligocki (Quick_Sim), Pavel Kropitz and Andrew Ducharme (their machines).
A candidate counts only from a blank tape. Mark every statement as proved, tested or observed.
