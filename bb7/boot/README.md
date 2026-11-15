# The boot of the claimed BB(7) champion (working notes, 15 Nov 2026)

Machine `1RB0RG_1RC1RB_0RD1RZ_0LE0LD_0LF1LE_1RA1LF_1LC0RB`, found by Jeff Ketchersid.
Digits: one per step, `2*state + symbol read`, written `0-9` then `a b c d`.

The claim tested here (Vishnu, from the BB(5) work): **a boot is always a smaller version of the machine.
It needs no wires and no words of its own.**

Status of each statement below: *checked* = compared with a plain run of the machine;
*proved* = follows from the Coq files `BB7Moves.v` / `BB7Halts.v`. Nothing else is claimed.

## 1. The roles in the first 35 digits

```
02468 bb | a1d 2468b | a1c | 47698b | a1c | 47698 | a03 ...
```

| block | role | what it does on the tape |
|---|---|---|
| `02468` | ring | one pass through A, B, C, D, E, each reading a blank |
| `bb` | filler | F walks left over ones |
| `a1d` | loader | takes 2 ones off the block and leaves one `10` pair on the left |
| `a1d 2468 b` | countdown line | the full word is `a1d 3(k) 2468 b(k+1)`; here k = 0, so the 3-run is absent |
| `a1c` | gate | same start as the loader, but G reads a 0 where the loader reads a 1: the block is used up |
| `47698b` | carry | turns pairs on the left into a unit on the right |
| `a03 ...` | looper | the build round; digit 35 is `3`, its filler, the last wire to appear |

Forks: `a1d` / `a1c` differ in what G reads. `2468` / `2476` differ in what D reads.

All 13 wires are seen by digit 35. Tables that give the champion's first N digits (everything free):
22 at N = 26, 8 at N = 36, and 2 (the champion and its mirror image) from N = 50 on (*checked*, `../transcript_to_table/prefix.py`).
A wire can be seen before its run has any length; the table is fixed once every word has appeared
with every run non-empty.

## 2. The words

| word | digits | meaning |
|---|---|---|
| `Round(n)` | `2476 9(n) 8a0 3(n)` | one build round; the block grows by 3 |
| `Close(n)` | `2468 b(n)` | close of a block of n |
| `Count(k)` | `a1d 3(k) 2468 b(k+1)` | one countdown line; lays one pair |
| `Carry(i)` | `a1c 476 9(i) 8b` | gate visit and carry |
| `Down(a)` | `Close(a) Count(a-2) ... Count(0)` | a block of a counted down: a pairs |

## 3. The boot, written by hand (*checked*: 319 of 319 digits, `boot_by_hand.py`)

```
0
Down(2)   Carry(1)                      a1c47698a03    Round(4)
Down(7)   Carry(1) Carry(2) Carry(2)    a1c476998a033  Round(5) Round(8)
Close(11) Count(9)  a1d 3(8) Round(9)   2476 9(13) 8b a1          -> gate, P = 13
```

The boot is one cycle, three times, growing: **count a block down, carry the pairs into units, build again.**
The restart after the gate is the fourth turn of the same cycle. No word appears in the boot that is not in the big run.

## 4. The small-size table: Jeff's machine started on a row of p pairs

Start tape `(10)^p [G reads 0]`. This is the state at digit 17 (p = 2) and at digit 141 (p = 7).

Carry (*checked*, p = 1 to 20): the first carry makes the last 1 and an end-mark; after that 2 pairs make one unit.
For p even the end-mark is `10` (a clean tape). For p odd it is `110`: one stray 1, which later joins the block.

| p | after the carries | what follows | outcome |
|---|---|---|---|
| 1 | nothing | `Close(4)` | 4 pairs |
| 2 | the last 1 | `Round(4) Close(7)` | **7 pairs** |
| 3 | the last 1, stray 1 | `Round(5) Close(8)` | 8 pairs |
| 4 | 1 unit | block ends even | halts, 414 steps |
| 5 | 1 unit, stray 1 | block ends odd at the last cell: restart, 13 pairs | block 14, gap 4, 3 units, last 1: halts (*proved*, `units_halt`) |
| 6 | 2 units | gate P = 12, even | halts, 3,200 steps |
| 7 | 2 units, stray 1 | gate **P = 13**, odd, last cell: restart | block 16, gap 4, **19 units**: the champion (*proved* to halt) |
| 8 | 3 units | block 12, gap 4, 1 unit, last 1 | halts (*proved*); P at the end about 1.7 x 10^10 |
| 9, 11, 13, 15 | units, stray 1 | odd block meets a wide gap: odd counter 43 | halts in the middle of the tape; P about 5.2 x 10^10 |
| 10, 12, 14, ... (even) | (p-2)/2 units | block 12, gap 4, (p-6)/2 units, last 1 | halts (*proved* up to 197 units) |

The champion's chain is two steps on this table: the first pass `02468bb` writes a block of 2 -> 2 pairs -> 7 pairs -> gate P = 13 -> restart.

Other first blocks: 1 -> 4 pairs -> halts at 414 steps. 3 -> 8 pairs -> one generation, halts.

## 5. What the table says

- **Parity.** p even: no stray 1, everything stays even, one generation, halt. p odd: the stray 1 makes the block odd.
  With 1 or 2 units the odd block reaches the last cell and the machine restarts (p = 5 and p = 7).
  With 3 or more units the odd block meets a wide gap first, becomes an odd counter, and the run halts in the middle.
- **Only p = 5 and p = 7 restart.** p = 7 gives the larger restart, and 7 is exactly what the boot lays.
  On its own table the champion sits at the best small value.
- **The level is set by how many pairs get laid.** For even p the run has (p - 6)/2 units in one generation:
  44 pairs would give 19 units, 46 pairs would give 20. The champion reaches about 45 pairs by its restart, not by its boot.
- **The big run obeys clean formulas; the boot lives in the squeezed sizes.** 1 -> 4 and 2 -> 7 look like a step of 3,
  but 3 -> 8 and 4 halts. Empty slots, a half unit and the end-mark decide these cases.

## 6. What this means for building a machine by hand

1. Write the grammar in roles and words with their slots (ring, filler, loader, gate fork, carry, looper; +3 per build round, 1 pair per countdown line).
2. The boot is the cycle of those words started from the block written by the first pass. Its sizes are not free: each cycle fixes the next.
3. The first 35 to 50 digits of that boot fix the table (`../transcript_to_table/draft.py` lists the tables).
4. The gate and the parity decide whether the chain ends in a restart, and how large.

Open: a rule for the squeezed sizes that does not depend on running the machine; and a second grammar
(Pavel Kropitz's machine) written the same way, to see what can change.

## Files

- `boot_by_hand.py` : the 319 digits from the words, compared with the machine.
- `small.py` : the machine started on p pairs; prints the words and the tapes. `python3 small.py 1 2 3 4 5 6 7`
- `rules.py` : the outcome of the long cases from the move rule, with exact integers.
