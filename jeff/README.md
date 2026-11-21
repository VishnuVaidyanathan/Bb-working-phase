# Jeff Ketchersid's champion in our stack terms (reading notes, 20 Nov 2026)

Machine `1RB0RG_1RC1RB_0RD1RZ_0LE0LD_0LF1LE_1RA1LF_1LC0RB` found by Jeff Ketchersid. `homes.py` reads its tape at every home
visit (state A reading 0) from a blank tape. Layout: block, then stores, two empty cells between them; two more empty cells = an empty level.

Observed (real run, 2 million steps):
* round: block +3, store in front -1
* store in front empty, a payer behind ("ticket"): fresh block 1; the old block +4 becomes the store in front; the payer pays 2
  (seen: 12 -> 38 -> 128 -> 398 -> 1208 ..., i.e. 3x+2, with stores 42, 132, 402, 1212 and the payer 52, 50, 48, 46, ...)
* nothing behind: block 39 -> a row of 22 stores (3, then twenties of 2, then 1)
* rows from a blank tape: [2,2,1], then 22 stores
* his halt (state C reading 1) is met when a payer that pays 2 at a time has 1 left - a gate in twos on the payers, not on the row end.

So his grammar is the same kind of stack as ours with four numbers: fresh block 1, round +3, old block +4, payer pays 2.
Not yet done: the complete rule set (two or more empty levels, the row-end rule in general) checked at every home visit, and the
arithmetic to the halt. Status of everything above: observed.

## Full rules (tested: rules.py thought experiments, then model.py against the real run)

On (block; stores), counting an empty level as a store of 0:
* round: front store > 0 -> block +3, front store -1
* ticket: g empty levels, payer d >= 2 -> block 1, g-1 fresh stores of 2, then a store of (block + 7 - 2g), payer d-2
* a payer of exactly 1 with a real store (2 or more) behind it -> HALT
* end of the row (payer 1, nothing real behind): block odd -> HALT; block even w -> new row of about w/2 stores of 2
  (block 3 and w/2+1 stores of 2 when g = 1; block 2, a store of 3 in place g-1, the rest 2s, when g >= 2), always ending in a store of 1.
model.py: 4,730 home visits of the real run (30 million steps) agree with these rules, 0 differ.

What the gate is, in these terms: the store made at a ticket is block + 7 - 2g. For g >= 2 it will be a payer that pays 2 at a time,
so it must be even, i.e. the block at that ticket must be odd. A ticket at depth 2 or more with an even block leaves a payer of 1 -> halt.
Second gate: an odd block at the end of a row.

## Rows and the start state (21 Nov)

From a blank tape started in A (the champion as published): rows of 3 stores, then 22 stores. 22 - 2 = 20, the number of arrows
in the published bound 3 ^(20) 3. So "arrows = stores in the halting row - 2" holds for his machine too (observed).

The same table started in another state on a blank tape (each is a different 7-state machine after renaming):
* B: halts at step 469.
* C, D, E, F, G: all fall into the same run: a first row of 4 stores, real tape after 20 million steps: block 6700, stores [1409, 28, 0, 1].
  The checked rules (model.py) carry this to the end of that row: block 52,301,766,007, odd -> HALT (tested by arithmetic, not run to the end).
  Had that block been even, the next row would have had about 26 billion stores.
So the boot (what the first row is) decides everything, and it is one parity away from an enormously longer run.

## Route 1: other first rows in the same grammar (boots.py, arithmetic on the checked rules)

22,376 small first rows tried (block 1..8, up to 4 stores of 0..6, then the end store 1):
16,704 halt before the row ends, 856 end with an even block and make a new row, 4,816 meet a case the rules do not cover.
567 of them are followed by a second row of 23 stores or more. Smallest examples (full list: boots_scan.txt):
  block 2, stores [2,2,1] -> block 40 -> 22 stores   (this is the champion's own boot)
  block 2, stores [2,3,1] -> block 40 -> 23 stores
  block 1, stores [3,2,1] -> block 46 -> 25 stores
  block 2, stores [0,4,1] -> block 82 -> 43 stores
  block 1, stores [1,4,1] -> block 100 -> 52 stores
  block 1, stores [1,6,1] -> block 316 -> 160 stores
So the grammar allows longer second rows from a first row that differs by one cell.
But his table makes exactly [2,2,1] from a blank tape, and no other start state gives a better first row (see above).
Whether those longer rows would halt, and where, is not computed yet (needs the arithmetic to the halt).

## How his 14 wires share the jobs (wires.py and a cell-by-cell trace, 21 Nov night; observed)

wires.py, 3,000,000 steps from a blank tape, events named by the checked rules:
* round (1,523 times) uses 9 wires: A0 B0 B1 C0 D0 D1 E0 E1 F0.
  A0 writes a cell and starts; B1 runs right over the block; B0 fills the first cell of the gap; C0 LOOKS at the second cell of the gap;
  D1 takes one cell of the front store (D0 if it is empty); E1 runs back left; E0 and F0 turn at the left end.
* payment between depths (8 times), the new row (once) and the start from a blank tape all use those 9 wires plus the SAME 4 more:
  A1, G1, G0, F1.  No other wire exists except the halt.
* halt = C1.  C is entered only from B0 (and from G0, where it always re-reads a cell A has just set to 0 - local argument).  So the halt
  is: B fills the first cell of a gap and the next cell is already a 1 = "the gap is one cell wide, not two".  It is the look the round
  makes on every trip.  A payer that pays 2 at a time leaves a gap of one or two: that is his test in twos.
So 9 (round) + 4 (everything else) + 1 (halt) = 14.

The cutter, traced on the block of 5 that makes his first row [2,2,1] (steps 95-178):
 phase 1 (peel): F0 writes 1, A1 and G1 erase two cells, B runs to the right end and adds a cell, F1 runs back: one `10` word per walk.
          It ends when G (or A) meets the right end: which of the two = the block odd or even.
 phase 2 (pair): G0 turns back, and the ROUND wires C0 D1 D0 E1 E0 F0 (with F1, A1, G0) walk left turning each `10 10` into `1100`:
          the stores of 2 with their two-cell gaps.
Compared with our stack (17 working wires: round 9, cutter 4, three cut endings, one runner): he has NO wire that is only a cut ending.
His peel ends on the home wire A0 or on G0, and G0 is also the wire that starts the pairing; his halt is not an ending at all.
