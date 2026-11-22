# Grammar of overlap (22 Nov) — paper reasoning, not tied to any machine

Vishnu's direction: learn the grammar, do not copy what another machine does.
Withdrawn: my plan "a 6-state round with three doors in the two-cell layout".
That was Jeff Ketchersid's shape, not a rule.

## What a wire can know

A wire sees two things only: the state, and one cell. So:

- **O1. A state is one remembered fact.** ("I am going out", "I took one and
  owe a second", "I am going home".) The tape remembers everything else.
- **O2. Two jobs can share a state exactly when they remember the same fact
  at that moment.** What they did before does not matter. What the tape
  looks like may differ; the cell read then splits them.
- **O3. A machine fits in n states when the story never needs more than n
  different facts held in the head.** This is the count to make on paper
  before any table.

## Ways to hold fewer facts in the head

- **O4. Put the fact on the tape (a mark).** Change a cell now; a later pass
  of the same wires reads it and branches. Cost: no state, one more pass.
- **O5. Never hold a count in the head.** A depth or a width is used up one
  unit per pass of the same loop.
- **O6. Let the act be the test.** Paying 2 needs "take one, take another".
  The wire that takes the second cell and finds none *is* the number test.
  Test and payment share one pair of wires; the halt costs half a state.
- **O7. Writes on turns are free.** Every turning wire may write. The
  constants of the story (gain q, fresh store size) come from the number of
  turns, not from extra states. So constants are tied to the trip's shape.
- **O8. A runner's state is a promise about the end of the run.** Two runners
  in the same direction are different states only if they must act
  differently at the end. If the end cells differ, one runner serves both.

## First fact count for our story (paper, not tested)

1. going out over the block
2. at the front: is there a store?
3. took one, owe a second (pay 2 / number test, by O6)
4. going home with the gain
5. front was empty: is there a payer behind?
6. going home after a payment (home action differs: land, do not extend)
7. nothing behind at all: make a new row

Seven facts, with nothing spare for depth or for the start. So facts must be
moved to the tape: 6 by a mark (O4) so that 4 serves both, depth by O5.
The work now is on this list, not on wires.
