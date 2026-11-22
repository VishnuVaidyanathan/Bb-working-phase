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
