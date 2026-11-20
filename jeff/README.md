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
