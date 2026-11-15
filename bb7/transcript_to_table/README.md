# From a transcript to a table (working notes, 15 Nov 2026)

Idea (Vishnu): do not search near a known machine. Write the transcript we want, and ask which table
supports it. The first digits of a run already fix the table.

## How many digits fix the champion's table (`prefix.py`)

Tables, with everything free, that give the champion's first N digits from a blank tape:

| N | wires seen | tables |
|---|---|---|
| 26 | 12 | 22 |
| 35 | 13 (all) | 112 |
| 36 | 13 | 8 |
| 50 | 13 | 2 (the champion and its mirror image) |

35 digits show every wire and next state; about 50 fix every write and move.

## The first digits are the grammar's own words at their smallest sizes

| machine | first digits | words |
|---|---|---|
| champion | `0` `2468bb a1d` `2468b a1` `c47698b a1` `c47698a03` | start, countdown size 2, countdown size 1, gate visit, open |
| base-4 tower | `0` `258bb a1d` `2477698a033` `259(5)8a033` | start, gate size 2, build round, first layer |

Working rule (two machines only): a blank tape looks like an empty counter, so the run begins with the
word that handles an empty counter, then one small build.

## Tools

- `draft.py "0 2468bb a1d 2468b a1 c47698b a1 c47698a03"` : tables that support a draft transcript, or the
  digit where no table can follow it. `x(n)` repeats, `?` is any digit.
- `fit.c` : roles fixed (next state of each wire), writes and moves free; lists tables that reach a
  gate-shaped tape `1 0 [G0] 1^P gap 1` from a blank tape.
- `units_scan.c` : looks for a row of `1100` units on the tape (the champion shows 20 at step 3755).

## Results so far

- Champion's roles: the only clean gate tapes reached are P = 13 (the champion) and smaller. No P >= 15.
- One wire sent to a different state (78 role sets): 4,160 tables reach a gate-shaped tape with P >= 14
  (largest 55), but none of them lays a row of units afterwards. The shape is the same, the behaviour is not.
- Cousins (8,219 undecided tables): only the champion lays units by a restart.

Open question: how to write the first 26 to 35 digits for a grammar we choose (pairs, fillers, loops, towers, gates).

## Sketch workbench (`sketch.py`)

The question (Vishnu): forget any known machine. Imagine a structure, write its transcript with what we know
(ring, fillers, loader, gate fork, carry, looper), and ask whether a table can play it.

`sketch.py` takes the blocks as imagined, with runs of any length (`x+`), exact runs (`x(n)`) and `?` for any digit,
and lists every table (all 7 states free) that plays them from a blank tape, or the block where it breaks.

Test on a description that is not the champion (a tower: the layer erases the block and rebuilds it, the gate walks over the block):

    python3 sketch.py "0 2 5 8 b+ a 1 d 2 4 7+ 6 9 8 a 0 3+ 2 5 9+ 8 a 0 3+ 2 4 7+ 6 8 a 0 3+"

32 blocks, no run length given, and exactly 8 tables can play it. One of them is the base-4 tower of `cousins/bb7/base4/`.
This matches the expectation that a properly written opening leaves about 8 to 12 tables.
