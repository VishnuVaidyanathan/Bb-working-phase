# Wires that do more than one job (working notes, 15 Nov 2026)

Question (Vishnu): in Jeff's machine `a1c` and `a1d` are different words, but the `a` and the `1` are the same wires.
The difference is in the combination. Which wires in each machine do more than one job?

## How a job is read

A wire is one digit (a state and the symbol it reads). Its job is read from the transcript: the digit before it and
the digit after it. Two different surroundings are two jobs. A run of the same digit counts as one use, so a filler
walking a long block is used once. Only surroundings seen at least 3 times in 1.5 million steps are counted.
`python3 wire_jobs.py TABLE` prints every wire with its jobs; `--all machines.txt` prints the table below.

There are two ways a wire gets a second job:

- **Fork**: the wire is followed by one state, and that state reads a 0 one time and a 1 another time. `a1c` / `a1d`.
- **Merge**: the wire is entered from two different wires. In Jeff's machine `032` and `d32`: B reading 1 is entered from A and from G.

## Jeff's machine (13 wires, 23 jobs)

| wire | jobs (share of its uses) | kind |
|---|---|---|
| 0 | `a03` | one job |
| 1 | `a1d` 65%, `a1c` 35% | fork: countdown goes on, or the block is used up (gate) |
| 2 | `324`, `d24` rare | merge |
| 3 (filler) | `032` 95%, `d32` 5% | merge: after a build round, or after a countdown line |
| 4 | `247` 91%, `246` 6%, `c47` 3% | fork and merge: build round, close, carry after the gate |
| 6 | `769` 94%, `468` 6% | fork and merge |
| 7 | `476` | one job |
| 8 | `98a` 92%, `68b` 6%, `98b` 3% | fork and merge |
| 9 (filler) | `698` | one job |
| a | `8a0` 92%, `ba1` 8% | fork and merge: open a build, or start a countdown line |
| b (filler) | `8ba` | one job |
| c | `1c4` | one job: the gate wire |
| d | `1d3` 96%, `1d2` 4% | fork |

Five wires have one job: the three fillers, the gate wire `c`, and `0`, `7`. The other eight are shared.
The rare jobs are the gate and the carry: `c47` is 3% of the uses of wire 4, `98b` is 3% of wire 8.

## All 24 machines

| id | jobs in all | forks (the next state reads 0 or 1, both used) | merges (entered from 2 or more wires) | wires that are both | wires with one job only |
|---|---|---|---|---|---|
| J2 | 23 | 6: 1468ad | 5: 2368a | 68a | 079bc |
| D1 | 28 | 8: 013789ab | 6: 016789 | 01789 | 245d |
| Q1 | 29 | 8: 46789bcd | 6: 45679c | 4679c | 012a |
| D2 | 26 | 7: 03579ad | 6: 02357a | 0357a | 1468c |
| D3 | 15 | 1: d | 1: 9 | - | 012345678ac |
| D4 | 26 | 6: 25679a | 6: 014789 | 79 | bcd |
| D5 | 32 | 9: 02578abcd | 7: 23458ab | 258ab | 19 |
| D6 | 26 | 7: 1345abd | 6: 1458ab | 145ab | 02679 |
| D7 | 32 | 9: 03478abcd | 7: 01238ab | 038ab | 59 |
| D8 | 27 | 9: 023568bcd | 7: 02389cd | 0238cd | 147 |
| D9 | 32 | 9: 0345679ab | 7: 0456789 | 045679 | 12c |
| T286 | 30 | 10: 01245689ab | 7: 45689ab | 45689ab | 37c |
| T246 | 31 | 9: 01234689a | 6: 014689 | 014689 | 57bd |
| T140 | 32 | 9: 0124579ab | 9: 012345789 | 0124579 | 6d |
| T93 | 30 | 8: 023589bc | 6: 0189bc | 089bc | 46ad |
| T46 | 26 | 6: 3789bc | 5: 3789a | 3789 | 01246d |
| T35 | 24 | 6: 0245bd | 5: 04567 | 045 | 139ac |
| T22 | 27 | 7: 0123568 | 5: 01238 | 01238 | 479abd |
| W5 | 30 | 8: 3569abcd | 7: 237abcd | 3abcd | 04 |
| S5 | 18 | 4: 069b | 4: 0369 | 069 | 124578 |
| J | 23 | 6: 1468ad | 6: 23468a | 468a | 079bc |
| P | 29 | 8: 023459ad | 8: 23456abd | 2345ad | 17c |
| T15 | 20 | 4: 35ab | 5: 3458a | 35a | 01269 |
| S6 | 25 | 7: 25789ab | 6: 045789 | 5789 | 16 |

(`J2` is the second table listed with the champion's size. Ids as in `catalogue.md`.)

## What it shows

1. **Every machine shares.** 13 wires carry between 15 and 32 jobs. The usual figure is 25 to 32: about two jobs per wire.
2. **Fillers are not shared; turns are.** The wires with one job are the fillers and one or two fixed steps.
   The wires with three or more jobs are always turn-around wires, where the head changes direction.
3. **The gate is a rare job of a common wire.** In Jeff's, wire 4 does the build round 91% of the time and the carry after
   the gate 3% of the time. In Pavel's, wire `a` is the filler `dad` 99% of the time and `dac`, the gate, in the rest.
   In the 4-arrow machine, wire 7 is the filler `379` and, rarely, `378`, the step into the reload.
   The machine has no wire set aside for the gate except the one that reads the deciding cell.
4. **Jeff's machine shares the least of the deep machines** (23 jobs; Pavel's 29, the 4-arrow machine 28). Its words are long
   and each wire sits in few of them. That fits its transcript: long smooth blocks.
5. **Forks and merges come in equal numbers**, 5 to 9 of each, and many wires are both. A wire that is both is a junction:
   several words pass through it and leave it in two directions.
6. **A machine with few jobs is a simple machine.** D3 has 15 jobs and its run in this window is plain long sweeps.
   The tower machines T15 and S5 have 18 to 20.

## For designing by hand

A word list is not enough to count wires, because words overlap. What can be counted is the junctions:
each fork needs one state that reads both symbols with both readings used, and there are only 7 states.
Jeff's machine has 6 forks, Pavel's 8, the 4-arrow machine 8. A tape story that needs more than about 9 places
where "the next cell decides" cannot fit in 7 states.
