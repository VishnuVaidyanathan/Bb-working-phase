# Building cousins of a champion from its grammar (BB(5) test)

**Question.** Given a champion's table, can we build its cousins? A cousin is
a machine that runs the same way, with the same kind of compression grammar,
to nearly the same size. It is not a neighbour that stops early.

**Answer for BB(5): yes.** Fix only the roles that the transcript grammar
names, let everything else vary, and run from a blank tape. This gives back
the champion and 13 of the known top halters, and nothing else.

**Answer for BB(7): we did not run it, and do not expect it to work.** See
the last section.

## The grammar, turned into wiring

One digit per step, `digit = 2*state + symbol`. So a digit is a wire.
The BB(5) champion `1RB1LC_1RC1RB_1RD0LE_1LA1LD_1RZ0LA` has this grammar:

| Role | Digits | Wires | What it fixes in the table |
| --- | --- | --- | --- |
| Pairs | `02`, `46` | `A0` then `B0`; `C0` then `D0` | `A0` goes to B, `C0` goes to D |
| Oscillator | `1 5 9` | `A1`, `C1`, `E1` | `A1` goes to C, `C1` to E, `E1` to A |
| Fillers | `7`, `3` | `D1`, `B1` | each stays in its own state |
| Halt | `8` | `E0` | the halt |

The roles fix the next state of a wire. They do not fix what it writes or
which way it moves.

## Test 1: the champion's exact skeleton

File: `src/skel.c`, result: `results/skeleton_test.txt`

Keep every next state of the champion, vary the write and the move of all
9 wires: 131,072 tables, each run from a blank tape.

| | |
| --- | --- |
| Halt | 42,633 |
| Longest | 47,176,870 steps, the champion |
| Second longest | 3,831 steps |

Inside its own skeleton the champion is alone. Grammar to wiring works, but
it gives no cousins.

## Test 2: do the known cousins share the roles?

File: `src/walk.py`, list: `results/bb5_top20.txt` (the top 20 BB(5) halters)

Reading the roles from each transcript, without being told the states:

| Machines | Fillers | Oscillator |
| --- | --- | --- |
| #1 (champion) | B, D | A, C, E |
| #7, #8, #9, #11, #12, #15 | A, B | C, D, E |
| #10, #13, #14, #16 to #19 | A, C | B, D, E |

Same roles (two fillers, one three-state oscillator on symbol 1), sitting on
different states. So a cousin keeps the roles and not the skeleton.

## Test 3: build from the roles alone

File: `src/roles2.c`, results: `results/roles_placement_A.txt`, `_B`, `_C`

    gcc -O2 -o roles2 roles2.c
    ./roles2 B D A C E 1 B      # fillers B,D; oscillator A->C->E; first wire 1RB

Fixed: the next state of the five 1-wires (from the roles), and the first
wire `1RB`. Free: every write, every move, every 0-wire's next state. A wire
is filled in only when the run from a blank tape reaches it; reaching an empty
wire counts as the halt. Speed filters: tape width at 300, 3,000, 20,000 and
200,000 steps, and machines that bounce in a regular rhythm are dropped at
2,000,000 steps. Runs go to 60,000,000 steps.

| Placement | Tables tried | Halt after more than 100,000 steps | Which |
| --- | --- | --- | --- |
| Fillers B, D; oscillator A, C, E | 1,348,502 | 1 | the champion (47,176,870) |
| Fillers A, B; oscillator C, D, E | 1,625,782 | 6 (printed 18, with the oscillator states renamed) | #7, #8, #9, #11, #12, #15 |
| Fillers A, C; oscillator B, D, E | 1,560,618 | 7 | #10, #13, #14, #16, #17, #18, #19 |

No other long halter came out. All the cousins found halt between 11,792,682
and 11,811,040 steps.

### What it does not cover

- #3 to #6 have a different shape: the three-state chain does not close; its
  last state falls into a filler. That variant was not run.
- #2 and #20 were not checked.
- The speed filters could in principle drop a real machine. They lost none of
  the known ones.

## Why this stays at BB(5) size

The BB(5) machines are flat: two fillers and one oscillator say almost
everything. Read the same way, the BB(7) champion has four fillers
(`B1, D1, E1, F1`), a six-state ring on symbol 0 (`A0 B0 C0 D0 E0 F0`), a side
state `G`, and the halt on `C1`. But its size does not come from those. It
comes from the stack of counters and the swap move on top
(see [`../bb7/design`](../bb7/design), sections 11 to 14), and the roles say
nothing about them. Also a BB(7) cousin would not halt within any number of
steps we can run, so "halts late" cannot be the test. This search was not run
for BB(7).

## Credits

The BB(5) champion is by Marxen and Buntrock; the top-halters list is from
the BusyBeaverWiki.
