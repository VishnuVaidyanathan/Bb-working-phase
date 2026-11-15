# Catalogue of 24 big machines (working notes, 15 Nov 2026)

The five machines of `README.md` plus the top halters of the BB(7) page of the bbchallenge wiki.
Each was profiled the same way. This is a first pass: a profile, not a full reading.

- **size**: as listed on the wiki (arrows) or from the tool.
- **rule levels**: how many levels of rules Shawn Ligocki's Quick_Sim needed to run it to the halt
  (`-r --exp-linear-rules --exp-meta-linear-rules --no-steps`, 150 seconds).
- **base** and **divisors**: read from the final formula the tool prints, for example `(7 + 3^x)/8` gives base 3, divisor 8.
  The divisor is where the gate's remainders come from.
- **numbers kept as**, **fillers**, **all wires by digit**: from a plain run of 800,000 steps (`tools/profile.py`).

| id | table | found by | size | rule levels (tool) | base | divisors | numbers kept as | fillers | all wires by digit |
|---|---|---|---|---|---|---|---|---|---|
| J | `1RB0RG_1RC1RB_0RD1RZ_0LE0LD_0LF1LE_1RA1LF_1LC0RB` | Jeff Ketchersid (claimed champion) | 3 ↑^20 3 (about 19 levels) | one move, depth on tape |  |  | units 1100; solid block | 3,9 | 35 |
| J2 | `1RB0RG_1RC1RB_0RD1RZ_0LE0LD_0LF1LE_1RA1LF_0LD0RB` | Jeff Ketchersid (second table) | same as J | no answer in 150 s |  |  | units 1100; solid block | 3,9 | 34 |
| P | `1RB0RA_1LC1LF_1RD0LB_1RA1LE_1RZ0LC_1RG1LD_0RG0RF` | Pavel Kropitz | 2 ↑^11 2 ↑^11 3 | 12 (Shawn Ligocki's run) |  |  | stripes (10)^m | pairs 25,ad | 103 |
| D1 | `1RB1RD_1LC0RD_0LG1LD_1RA0RE_1LF1LA_0LC1LE_1RZ0LE` | Andrew Ducharme | 4 arrows | 5 | 3 | 2 | stripes (10)^m; solid block | pairs 8b | 56 |
| Q1 | `1RB1LE_1RC1RZ_1LD1LC_1RF0LE_0LC0LD_0RG1RG_0RC1RA` | @prurq | 3 arrows | no answer in 150 s |  |  | solid block; gap of zeros | pairs 79 | 66 |
| D2 | `1RB1RA_0LC0LG_0RD1LB_1RD1RE_1RF0RA_1LC1RZ_0RF0LD` | Andrew Ducharme | 3 arrows | 4 | 2 |  | stripes (10)^m | mixed | 35 |
| D3 | `1RB1LE_1LC0RA_0LD0LC_1RE1LD_1RF0LE_0RG1RZ_1RG1RA` | Andrew Ducharme | 3 arrows | no answer in 150 s |  |  | solid block; gap of zeros | c,5 | 63 |
| D4 | `1RB0RD_1RC1RZ_1LD1RA_0RE1LE_0LA0LF_0LG0LD_1RC0LA` | Andrew Ducharme | 10↑↑10 10↑↑10 10↑↑3.2 | no answer in 150 s |  |  | units 100; solid block | mixed | 63 |
| D5 | `1RB1RD_1RC1RA_1LA0RB_1RZ0RE_1RF1RE_1LG0LC_0LC0LF` | Andrew Ducharme | 10↑↑10 10↑↑10 10^18783 | 3 | 3 | 2 | stripes (10)^m | pairs ad,25 | 71 |
| D6 | `1RB1RF_1RC0RF_1LD1LA_0LE1LE_1LG0LA_1RE0RC_1RZ1LC` | Andrew Ducharme | 10↑↑10 10↑↑65533 | 3 | 2 |  | stripes (10)^m | mixed | 44 |
| D7 | `1RB1RC_1LC0RA_1RA1RD_1RZ0RE_1RF1RE_1LG0LB_0LB0LF` | Andrew Ducharme | 10↑↑10 10↑↑9840 | no answer in 150 s |  |  | stripes (10)^m | pairs ad,03 | 37 |
| D8 | `1RB0RF_1LC1LG_0LE1LD_1LE0LA_1RA0LB_1RZ1RG_0LB0RE` | Andrew Ducharme | 10↑↑10 10↑↑2453 | 3 | 2 | 5 | stripes (10)^m | mixed | 72 |
| D9 | `1RB0RG_1LC1RE_0RD1LD_0LE0LF_1RA0RC_0LA0LC_0LD1RZ` | Andrew Ducharme | 10↑↑10 10↑↑109 | no answer in 150 s |  |  | units 100; solid block | mixed | 53 |
| T286 | `1RB1RF_0RC1RG_1LD1LE_0LE1LD_0RF0LC_1RA0LC_0RF1RZ` | Terry Ligocki | 10↑↑286 | 2 | 2 | 9,3 | stripes (10)^m; solid block | pairs 1a,59 | 25 |
| T246 | `1RB0LE_1RC0RA_1RD0RC_1LE1LD_1LA0LF_0LA0LG_1RZ0RD` | found in @Iijil's range | 10↑↑246 | no answer in 150 s |  |  | stripes (10)^m; units 1100; solid block | pairs 03,18 | 104 |
| T140 | `1RB0LC_1LC0LD_1LA1LB_0LG1RE_1LD0RF_0RA1RE_1RZ1LC` | found in @stokastic's range | 10↑↑140 | 2 | 3 | 40,8 | stripes (10)^m; units 1100; units 1110 | pairs 14 | 7478 |
| T93 | `1RB0LF_1RC1RA_1RD0RG_1LE1RZ_1LA0LF_1RA1LE_0RE1RG` | found in the Iijil / Terry Ligocki range | 10↑↑93 | no answer in 150 s |  |  | stripes (10)^m; units 1110; solid block | pairs 9b,03 | 3324 |
| T46 | `1RB0LG_1RC0RF_1LD1RZ_1LF0LE_1RA1LD_1LG1RE_0LB0LB` | Terry Ligocki | 10↑↑46 | 2 | 2 | 9,3 | stripes (10)^m; solid block | mixed | 24 |
| T35 | `1RB1RA_1RC0LC_0LD1LG_1LF0LE_1RZ1LF_0LA1LD_1RA1LC` | listed May 2025 | 10↑↑35 | 2 | 2 | 9,3 | units 110; solid block | 1 pairs 5d | 39 |
| T22 | `1RB0RF_1LC0RE_1RD1LB_1LA1LD_0RA0LE_1RG0LB_1RZ1RB` | Shawn Ligocki | 10↑↑22 | no answer in 150 s |  |  | stripes (10)^m; units 1110; solid block | pairs 25 | 261 |
| T15 | `1RB0LD_1RC0RF_1LC1LA_0LE1RZ_1LF0RB_0RC0RE` | Pavel Kropitz (6 states) | 10↑↑15 (6 states) | 2 | 3 | 8,2 | gap of zeros | 4 | 20 |
| W5 | `1RB---_1RC0LG_1LD1RB_1LF1LE_1RZ1LF_1RG0LD_1LB0RF` | Kropitz, Michel, Wythagoras | 10↑↑5.9 | 2 | 2 | 27,9 | stripes (10)^m; units 110 | pairs ad,3c,6b | 29 |
| S5 | `1RB0LA_1LC1LF_0LD0LC_0LE0LB_1RE0RA_1RZ1LD` | 6-state, from Shawn Ligocki's collection | 10↑↑5 (6 states) | 2 | 2 | 9 | solid block; gap of zeros | 8,5 | 48 |
| S6 | `1RB1RA_1RC1RZ_1LD0RF_1RA0LE_0LD1RC_1RA0RE` | BB(6) champion (rules by mxdys) | 3 arrows (6 states) | 3 (tick, epoch, restart) |  |  | units 100; solid block | 1 | 214 |

## What the catalogue shows

1. **Stripes are the usual way to keep numbers.** 14 of the 24 keep numbers as `(10)^m`. Solid blocks with gaps (Jeff's way) are the minority.
2. **Units come in several shapes**: `100`, `110`, `1100`, `1110`. The shape is not fixed by anything we can see yet.
3. **Pair fillers go with stripes.** `25`, `ad`, `03`, `79`, `8b`, `59`, `1a`: a pair of digits that walks a stripe two cells at a time.
4. **The base is 2 or 3 in every formula the tool printed.** (Our base-4 tower is the only 4, and it does not halt.)
5. **The divisors are 2, 3, 5, 8, 9, 27, 40.** These are the gates: the run ends on a remainder. Powers of 2 and 3 are the common ones.
6. **Above 2 rule levels the levels are on the tape.** D1 (5 levels), D2 (4), D5, D6, D8 (3) and P (12) all keep striped groups; J keeps units.
   None of them has that many separate rules in its 13 wires.
7. **"All wires by digit 35" holds for only some.** 9 of the 24 show every wire by digit 40. 11 need between 40 and 110.
   T93 needs 3,324 digits and T140 needs 7,478: a machine can run for thousands of steps as a smaller machine before its last wire is used.
8. **J2**, the second table on the wiki with the champion's size, differs from J in one wire (G reads 0). Its tape looks the same.

## D1, the 4-arrow machine (first look)

`1RB1RD_1LC0RD_0LG1LD_1RA0RE_1LF1LA_0LC1LE_1RZ0LE`, found by Andrew Ducharme. Quick_Sim runs it to the halt in under a second, with one rule on each of 5 levels.

Tape at its rarest wire (A reads 1): `111 (10)^3 1 (10)^G [head] 1^n 0001`.

- G goes down by 1 per round and n -> 3n + 12 (seen: n = 9, 39, 129, 399, 1209).
- When G is used up, the group to its left loses one and a new G is loaded from n.
- Later the tape holds four groups (3, 15, 262, 996): the levels are a stack of striped groups, as in P, but only a few of them.

It is the closest known machine to the 6 or 7 arrows we want to build, and small enough to read completely. Not done yet.

## Files

- `machines.txt` : the 24 tables with their ids.
- `tools/profile.py`, `tools/catalogue.py` : the scripts.
