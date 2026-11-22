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
