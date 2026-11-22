# Our own tripling engine: first sketch (22 Nov)

Why: an adding stack (ours) has a fixed tail map and can do one iteration at most.  A multiplying engine (the block becomes a store)
gives a class that depends on the number.  Gate rule: multiplier 3 needs a test in twos.  Built from the wire budget, in our own stack
layout (solid block, stores of 1s, ONE empty cell between them) - not from Jeff Ketchersid's table.

Skeleton (7 states, 2 wires still open, written ???):

    A: 1RB ???    B: 1RC 1RB    C: 1RE 0LD    D: 1LA 1LD    E: ??? 1RF    F: --- 0LG    G: 0LA 1LG

Jobs (each wire has one job; 11 working wires + the halt):
* round, 6 wires: A0 writes a cell, B1 runs right, B0 fills the gap, C1 takes one cell of the front store, D1 runs back, D0 writes a
  cell and steps to home.  Block +3, front store -1.
* look: C0 = "the front store is empty".
* payment between depths, 4 wires: C0 fills the second empty cell, E1 steps over the payer's first cell, F1 erases its second cell,
  G1 runs back left, G0 leaves an empty cell at the left end and steps to home.  The old block (with the 2 filled cells and the payer's
  first cell) becomes the front store; a new block starts from nothing; the payer has paid 2.
* halt: F0 = "the payer had exactly one cell left" - a test in twos, made by the payment itself.
* open: E0 = "the payer is empty" (next level, or end of the row), and A1 (never reached so far).

Tested on hand-made tapes (block, front store, payer), with the two open wires left as stops:
    block 3, stores [2,4]: payments at blocks 11, 41, 131 (payer 4, 2, 0)  -> stops on E0 (payer empty)
    block 3, stores [2,5]: 11, 41, 131 (payer 5, 3, 1)                     -> stops on F0 = HALT (odd payer)
    block 3, stores [2,6]: 11, 41, 131, 401 (payer 6, 4, 2, 0)             -> stops on E0
    block 3, stores [2,7]: 11, 41, 131, 401 (payer 7, 5, 3, 1)             -> stops on F0 = HALT
    block 2, stores [1,6,4]: 7, 29, 95, 293                                -> stops on E0
So block -> 3*block + 8 at every payment (tested): it triples, and an odd payer halts while an even payer goes on.
Not done: what E0 and A1 must do so that an empty payer hands over to the next store (depth) and a finished row makes a new row;
the start from a blank tape.  Nothing here is proved.

## The two open wires of skeleton 1: all 784 fills (tapes.c, 22 Nov) - no tower, with the reason

Compared with Jeff Ketchersid's table wire by wire: only the common first three wires (`1RB`, `1RC 1RB`) agree; his stores sit two cells
apart, his look and his eater are two states and his left turn takes three wires - a different machine.
On paper: a payer of size p gives p/2 triplings = one exponential.  A tower needs the old block to become the PAYER (then the next block
is about 3^(old block / 2)); in this layout that means two empty cells at the left end instead of one.
Run: every fill of A1 and E0 on tapes block 3, stores [2,4,q] for q = 2,4,6,8, on [2,2,2,2] and on a blank tape, 30,000,000 steps each
(columns: H steps ones payments, or R ones payments; skeleton1_784_fills_on_hand_tapes.txt).
594 fills do not halt on the first tape; 104 halt in the same number of steps for every q (the third store is never used);
86 take about 9 times more steps for each +2 of q (the last of them running out of the step limit): one more tripling per unit paid.
That is a single exponential.  The one fill that looked like a blow-up (A1=1LG, E0=0RF) was read by hand: the deep payer pays 1 per
tripling (blocks 132, 399, 1200, 3603), still one exponential.  Towers: 0.
Reason: with the left-end wire fixed (G0 = `0LA`, one empty cell) no fill of two wires can make the old block a payer.  Tried on paper:
sending the left return through E0 to leave two empty cells - it does so at every payment, and the machine then lays a store of 4 and
pays 2 for ever, running away to the left.
Open design question: a second kind of left return (one empty cell after a plain payment, two after a deep one) within 14 wires.
