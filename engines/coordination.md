# Coordination grammar: design the engine on paper first (Vishnu's direction, 22 Nov)

Building wire by wire loses what is needed.  Describe an engine by WHAT HANDS WHAT TO WHAT, check the four questions on that
description, and only then count wires.

## Roles
block (the number being grown) - front store (paid 1 per round) - payer (pays when the front store is empty) - deeper stores -
the row (how many stores there are).

## The hand-overs, and what each one buys
| Hand-over | Growth it gives |
|---|---|
| round: front store pays 1, block +K | adding |
| block -> front store | multiplying by K |
| block -> payer (the store one level deeper) | K to the power of the block |
| block -> the deepest EMPTY level, whatever its depth | one more arrow for every level |
| block -> the number of levels (a new row) | towers over towers |
| a number -> a test in strides of s (s and K share no divisor) | a halt that depends on the number |

## The four questions, asked of the description
1. Deep?  Only if the block lands in the DEEPEST empty level.  (Skeleton 1 always landed it in the front store: one exponential -
   which is what its 784 fills showed.)
2. Tower over towers?  Only if at the end of a row the block becomes the number of levels.
3. From a blank tape?  The rules applied to the empty list must give a list that grows; the first row must pass the tests.
4. Seven states?  Depends on how the "which level" fact is carried.  See below.

## What the engines we know do, in these words
* Jeff Ketchersid's (checked rule, jeff/model.py): with g empty levels and a payer of 2 or more: block 1, then g-1 fresh stores of 2,
  then the old block (+7-2g), then the payer less 2.  So the old block lands exactly at level g, the deepest empty one, and the
  empty levels above it are refilled.  One rule covers every depth.  Row end: block even -> a row of block/2 stores.
* Pavel Kropitz's and g4: the same shape with x2 (g4: k # n # -> k-1, n -> 2n+4; when k is used up two more bars are taken).
* Our stack: at every exhaustion the block is cut into block/m stores - the block becomes the number of levels every time.  Towers, but
  every store adds a multiple of m, so the class is fixed by the tail (one iteration at most).
* Skeleton 1 (tripling): block -> front store only.  One exponential.

## How the depth is carried without a wire for it (read from his rule and his cutter trace; to be checked by one trace for g > 1)
The fresh stores cost the old block 2 cells each (the "-2g"), and the cutter is a peel: one store cut at the left, one trip to the
right end, back.  Each trip to the right fills one empty level.  So the number of peel trips = the number of empty levels: the count
is carried by repeating a loop, one trip per level, not by a state or a mark.
Our own stack has the same peel loop.  The whole difference between our adding stack and a multiplying engine is the STOPPING RULE
of the peel:  ours stops when the block is used up;  the multiplying one stops when the empty levels on the right are used up
(the runner meets the payer), and the rest of the block stays whole as the store at that level.

## Paper design task that follows
An engine of our own = our stack's round and peel, with the peel's stopping rule changed to "until the runner meets the payer",
a payer that pays in strides sharing no divisor with the round, and a row end that hands the block to the number of levels.
Each line of that is to be checked on paper against the four questions before any table is written.

## First paper result (22 Nov): our own 7-state stack already has the landing rule; it only pays in ones

Test of the stopping rule on our own stack `1RB1RG_1RC1RB_0LF0LD_1LC1LD_1LD0RB_0RA1LF_1RZ1RE`, hand-made tapes, home visits (block; stores):
    (7; 0 4 3) -> (2; 8 3 3)          one empty level: new block 2, the old block (+1) becomes the front store, the payer pays 1
    (26; 0 3 3) -> (2; 27 2 3)        the same again; in between the block went 2 -> 26 = 2 + 3*8: it MULTIPLIES by 3
    (6; 0 0 4 3) -> (2; 2 5 3 3)      two empty levels: a fresh store of 2 on top, the old block lands at level 2, the payer pays 1
So our stack's rule is:  g empty levels, payer >= 1  ->  block 2, g-1 fresh stores of 2, then (old block + 3 - 2g), payer - 1.
Jeff Ketchersid's checked rule:                          block 1, g-1 fresh stores of 2, then (old block + 7 - 2g), payer - 2.
Same coordination grammar, different numbers.  (Correction: "our stack only adds" was wrong.  It adds inside a store and multiplies at
every payment.  What I saw as a fixed class has another cause, next paragraph.)

Why paying in ones can never give a number test (paper argument, parity only):
each payment turns block b into 2 + 3*(b + 3 - 2g), which is odd when b is even and even when b is odd: one flip per payment.
A payer of size P pays P times: P flips.  A landed block has size b+3-2g, i.e. the opposite parity to b; as a payer it gives that many
flips, so the block comes out with a parity that does not depend on b.  Every dependence on the number cancels itself.
With payments of 2 a payer of size P gives P/2 payments, and whether P/2 is odd or even depends on P in fours: the number survives.
So in this grammar the stride of 2 is forced, for the base halt and for the row-end test alike.

What is fixed and what is free:
fixed by the grammar - round +3, pay 2, land the block at the deepest empty level, refill above it, row end hands the block to the
number of levels.  Free - the small numbers: the size of the new block, the offset added to the landed block, the fresh store size,
the shape of a new row, and the start.  Jeff's machine is one choice of those numbers; its weak point is its start (first row 3 stores).
Next on paper: run the GRAMMAR (not a machine) from the empty list for each choice of the small numbers, and see which choices give a
long first row that passes the tests.

## The grammar run for a grid of the free numbers (bench.py, 22 Nov) - grammar level only, no machine yet

Check of the bench: with Jeff Ketchersid's numbers (new block 1, added 7) his first row, block 2 stores [2,2,1], ends with block 40,
as in his real run; his second row (block 3, 21 stores of 2 and a 1) is too big to work exactly, as it should be.
Short rows with his numbers and row block 3: 1 store -> 9, 2 -> 43, 3 -> 1,412,147,682,397 (odd: halt), 4 -> too big.
Grid: new block 0..3, added 1..9, row block 2 or 3, row offset 0 or 1, started as if a row had ended with block 2, 4 or 6: 432 chains
(bench_grid_432_choices.txt).  184 end on an odd block (power halt), 103 on the base halt, 77 get too big inside a row, and
68 (34 different choices of new block / added / row block) do this: a first row of 3 stores is worked exactly, ends on an EVEN block,
and the next row has that block / 2 stores - from 132,861 up to 24,783,191,826,202 stores.
Of the 34, 15 also keep long rows alive as far as the bench can follow (rows of 4, 5, 6, 9, 30 stores run until the numbers are too
big, no base halt): new block 0 with added 2,4,6,8 (row block 2); new block 1 with added 4,6,8 (row block 3); new block 2 with added
2,3,4,5,6,7,8,9 (row block 2).
One of them is our own stack's numbers (new block 2, added 3) with the payment changed from 1 to 2: second row 25,110,586 stores.
What this is not: a machine.  No table is known to realise any of these choices; whether the long second row halts is not known;
the first row of 3 stores is assumed, not produced from a blank tape.

## Where can "pay 2" live in our own stack?  Paper tries (22 Nov) - not in the eater

How our stack pays today (trace): a payment is one peel trip (cut a store at the left, run right, fill one empty cell) followed by ONE
step of the round's eater on the payer.  The same wire (C1) eats in the round, pays the payer, and shifts the cut store back.
1. "The eater eats 2" (C1 erases a cell and steps right, a new state erases the next and looks; 8 states,
   `1RB1RG_1RC1RB_0LF0RH_1LC1LD_1LD0RB_0RA1LF_0LD1RE_---0LG`, run with home_visits.py):  (4; 4 4 3) -> (7; 0 2 4 3) -> (2; 0 7 0 0 4 3) ...
   Fails by geometry: the store's edge retreats 2 cells per round while the block advances 1 into the gap, so empty cells pile up
   between them; and the wire's third job (shifting the cut store back) is broken.  From a blank tape it stops at step 84.
2. "Step over one, erase one" in the eater (on paper): the geometry holds (block +2 on the right, store -2), but then EVERY store is
   tested in twos when it runs out, also every landed block used as a front store.  With +4 per round the parity never changes (blind);
   with +3 it is tested at every payment - a run of passes only as long as the number has even halves, i.e. a few steps.  Too many tests.
3. So the round must eat 1 (no test) and only the payment must pay 2 (test).  One wire cannot do both in the one-empty-cell layout:
   the payment needs its own "step over" wire, its own "erase" wire and the look, and something to tell it apart from a round.
   Tries at paying before the cut (C0 fills and a new state erases one payer cell first): each erased cell costs one more peel trip,
   so the payer is turned into fresh stores one by one - not a payment of 2.
Count for our layout: our stack's 14 wires, minus the old halt wire, plus step-over, erase, look, and a second right-runner (2 wires)
to mark "this is a payment" = 18 wires = 9 states.  With two empty cells between stores the look is free (the width of the gap after
paying), which is Jeff Ketchersid's layout.
Honest position: the grammar is clear on paper; a 7-state realisation of "pay 2" in OUR layout is not found, and the count says
it does not fit as tried.

## "A count decides, not a coin": iterated rows that must halt (22 Nov) - grammar checked on the bench, layout problem found

Idea (from Vishnu's note that the power halt has its own arithmetic): swap the two meanings of "the payer has 1 left".
Today (Jeff Ketchersid's rule): a store behind -> halt; nothing behind -> block even: new row, block odd: halt (one coin toss per row).
Swapped: a store behind -> NEW ROW (the block becomes the number of levels, put in front of what is behind, which pays 2);
nothing behind -> HALT.  Every pair of cells behind is one more row; what is behind never grows, so it must halt.
bench_count.py, smallest cases with a slow toy round (+1): block 2, stores [2,1] with [2] behind: 1 row then halt; with [4] behind:
2 rows then halt; with [2,2] behind: 2 rows then halt.  With the real round (+3): the first row of one store ends with block 9 and
the next row has 4 stores - already too big to follow.  The structure is as intended.

Step 2, his wires in the three situations (hand tapes, traced):
* payer 1 with a store of 4 behind, block 5 or 6: HALT on C1, last wires ... F0 A1 G1 B0 C1
* row end, block 5 (odd): HALT on C1, last wires ... A1 G0 C0 D1 D0 E1 E0 F1 F0 A1 G1 B0 C1
* row end, block 6 (even): new row (3; 2 2 2 2 1) after 317 steps
Both halts are the same wire and the same local event: B fills a cell and the next cell is already a 1.  With a store behind, that is a
COLLISION: every peel trip adds one cell at the right end of the block, and the block runs into the store behind it.
So in this layout a new row can only be laid into empty tape.  A row "in front of what is behind" has no room: each new store needs 4
cells and the block gives 2.  The swap is not a change of two wires here; it is against the geometry.
Consequence for the layout: the count that decides must not sit behind the row.  It has to sit on the other side of home (left of
the block), where the row maker never goes, or the row maker must take its room from the store behind (as our own one-cell stack
does: there each peel trip takes one cell from the next store).

## Two-sided layout: a count on the left of home (22 Nov, hand tapes on the two-cell engine) - no safe place there either

The row end at the left, traced: the pairing walks left; with an even block it ends with E0, F0 (writes the home mark), A0 = home with
the new row; with an odd block one `10` word is left over, a peel step (F0 A1 G1) erases two cells, B fills, C meets the first store:
halt.  The cells left of home are part of this: they hold the home mark, and the last steps run over them.
Test: a count of c cells put on the left, 1, 2 or 3 empty cells before the home mark, then a row end with an even block (6; 0 1):
* 1 empty cell: the count is swept into the first block of the new row (block 3+c: 4,5,6,7,8,9 for c = 1..6).
* 2 empty cells: c = 1 gives a row one store longer; c = 2..6 HALT (steps 322..330).
* 3 empty cells: the row is made, the count is still there at the first home visit, and it is swept into the block at the next round
  (block 7+c).
So whatever stands on the left is either swallowed by the block within a round or causes a halt at once.  It cannot be a count that
pays once per row and stays.

What the paper work now says about "how many rows":
a new row can only be laid into empty tape (behind = collision, left = swallowed).  So nothing that counts rows can be stored as a
number beside the row.  The number of rows can only be decided by
 (a) a coin: a number test on the block at the row end (Jeff Ketchersid's engine), or
 (b) a small clock carried in a SHAPE that the row maker rewrites each time (Pavel Kropitz's lead word: row at 3, halt at 4; our own
     9- and 10-state machines: the tail of the row, two steps).
Iterated Ackermann in 7 states therefore means: a coin that comes up right more than once, or a shape clock with more than one
row slot.  Both known 7-state engines have exactly one row in them from a blank tape.
