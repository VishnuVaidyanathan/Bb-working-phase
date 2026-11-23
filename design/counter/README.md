# Counter arithmetic behind the door (23 Nov) — Vishnu: "design that counter arithmetic behind the door and make it rarer"

## A working example we already have: the 8-state table from last night (observed on hand-cut tapes)

`1RB1RG_1RC1RB_0LD0LH_0RA1LD_1LA1RF_1RZ1RA_0RH0RB_1LC1LH`
From a blank tape, after 100,000 steps the tape is: block 477, store 42,
**fast counter 16**, then a **slow counter: a row of 62 single cells**, then 2.

`runout.py` / `runout2.py` cut the counters short by hand and run on
(a look at the rules, not a run from blank):

| moment | what the machine does | seen |
|---|---|---|
| one unit of the fast counter | the block about triples (605 → 1,818 → 5,463) | fast counter 3 → 2 → 1 |
| fast counter runs out | one cell of the slow counter is used; the old block is set aside as a store; a **fresh fast counter of 16** appears | `1820 _ 1x2 2` → `603 16 1818 1 2` |
| slow counter runs out too | the block is counted out, cell by cell, into a **new slow counter as long as the block**; the block is rebuilt; a fresh fast counter of 15 | `1820` → `1x1817 … ` → `1820 15 1x1817 2` |
| halt | not seen at any of these moments | — |

So this table has three nested levels: block × 3 per fast unit; fast counter
refilled (16) per slow unit; slow counter refilled from the block itself
when it runs out (rows of rows). That is why Quick_Sim reaches four arrows.
But nothing in it ends the game: on these tapes the halt wire (F reads a 0
right after E reads a 1) never fires. It probably never halts (not proved).

## What this teaches for the design

- A counter kept as a row of single cells, used one cell per event, works
  and costs few wires. So does "refill the counter from the block".
- The rarity ladder is real: fast unit → fast run-out → slow run-out. Each
  is one level rarer than the one before.
- The halt belongs one level above the rarest event that still repeats:
  **"when the slow counter runs out, take one cell from a third, small
  counter; halt when that is empty."** In this table the slow run-out always
  refills, so the ladder has no top.
- For Vishnu's grammar (loop of five, door → F → G → halt): F = the fast
  run-out job, G = the slow run-out job, and G's second wire = the halt when
  the last counter is empty.
