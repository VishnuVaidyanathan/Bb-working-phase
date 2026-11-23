# Frame around our own round + payment transcript (23 Nov)

The transcript is in `compile/round_transcript.md`. Table of the draft:
`1RB1LA_1RC1RB_0RC0RD_1RZ0LE_1LF---_1LG1LA_0LA1LG`.

## Paper reading of the draft (tested on hand tapes)

- Landing: block w, front store empty, payer d → (3; w+2; d−2).
- A store S gives the block 3 + 3S/2. So each landing multiplies by 3/2,
  and a payer d gives about (3/2)^(d/2): **one exponential, counted by the
  payer.** That is one arrow.
- For a tower the big block must land as a **payer**, not as a front store.
  In this layout that means: on a deep landing, leave a gap **two** cells
  wide at the far left instead of one. Then the new block finds "front store
  empty" at once and the big number behind it pays.
- The draft does not do that. With two empty levels it makes a store of 2
  on the right and goes home as a plain round ((w; _ _; d) → (w+2; 2; d−2)).
  No depth.

## depth.c — search inside the frame

Fixed (the words of the transcript): both fillers, both takes, the home
digit, the gap fill, the halt on digit 6, the left walker G1.
Open: what digit 4 (C0), digit a (F0) and digit c (G0) do, and where digits
8 and b point. 1,075,648 tables.
Test: hand tapes (3 2 2 e). Depth shows as the run getting enormously
longer when e grows by 2.

First pass (20,000 steps a tape): 663,444 tables stop on e=4; in 663,436 of
them e=6 is less than 30 times longer; 8 kept, none of them a real depth
(e=6 runs past the limit but e=8 stops early, so it is a loop, not growth).
Longer pass running.

## Longer pass — result: zero (tested)

300,000 steps a tape, starting sizes e = 2 and e = 4, all 1,075,648 tables.
- About 663,440 tables stop on the smallest tape. In all but 13 of them the
  next tape is less than 30 times longer.
- The 13: ten have a middle tape of about 74,000 steps and then a short one
  for the next size (not growth with depth); three run past the limit on
  both larger tapes, and by transcript they erase the block leftwards and
  run away (junk).
- No table in the frame shows depth.

Reading: with the transcript's words fixed, changing what digits 4, a, c do
is not enough. The deep landing ("leave a two-cell gap at the far left")
needs its own word, and the table has no free digit for it. Something has to
give up its place.
