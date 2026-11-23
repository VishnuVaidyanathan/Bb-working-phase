# A round written as a transcript (23 Nov) — Vishnu's digits; tested on hand tapes with `transcript.py`

Digits: A0=0 A1=1 B0=2 B1=3 C0=4 C1=5 D0=6 D1=7 E0=8 E1=9 (then a b c d).
Even digit = the head read a 0. Odd digit = the head read a 1.

## Rules of the digits

1. **A repeated digit is a filler.** It must point to its own state
   (3 repeats, so B1 = `1RB`). (Vishnu's rule.)
2. **A filler ends with its partner digit, the same state.** A run of 3s ends
   with 2; a run of 1s ends with 0. So the partner is always the turn or the
   fill at the end of the walk.
3. **Even digits give, odd digits take.** An even digit that writes 1 adds
   one cell. An odd digit that is not a filler and writes 0 takes one cell.
   Gain of the round = number of giving even digits. Payment = number of
   taking odd digits.
4. **Two takes in a row must be two different states.** If a take pointed to
   itself it would be a filler that eats the whole store, with no count.
5. **The second take's partner is the number test.** If the second take
   finds a 0, the store had exactly one cell: that even digit can be the halt.

## The round: pay 2, gain 3

    0  3 3 3 3 3  2  5  7  8  1 1 1 1 1 1 1      (5 6) -> (8 4)

| digit | wire | job |
|---|---|---|
| 0 | A0 `1RB` | home: give one cell, turn right |
| 3… | B1 `1RB` | filler: walk right over the block |
| 2 | B0 `1RC` | partner of 3: give one cell into the gap |
| 5 | C1 `0RD` | take the first cell of the store |
| 7 | D1 `0LE` | take the second cell, turn left |
| 8 | E0 `1LA` | give one cell (keeps the gap one wide) |
| 1… | A1 `1LA` | filler: walk left to home |
| 0 | A0 | partner of 1: next round |

Tested: (5 6) → (8 4) → (11 2) → (14), then stops on digit 4 (C0, front
store empty: free). (5 5) → (8 3) → (11 1), then stops on digit 6 (D0: the
number test). Three even digits give 3, two odd digits take 2.

Free after the round: digits 4 (front store empty), 6 (number test), 9.

## Same state or different state?

- 3 and 2: same state (filler and its end). 1 and 0: same state.
- 5 and 7: must be different states (rule 4).
- 8 could share a state with 4: put E0's job on C0 (`1LA`). Then the round is
  4 states: `0 3… 2 5 7 4 1…`. Tested: same round. But then "front store
  empty" also gives a cell and goes home, so the block just grows by 3 for
  ever ((14) → (17) → (20) …). The signal "front store empty" is lost.
  So 8 keeps its own state unless the layout gives another signal.

## The payment word, drafted from digit 4 (23 Nov) — tested on hand tapes

Digits: a = F0, b = F1, c = G0, d = G1.

Round now (one digit added, b):   `0 3… 2 5 7 8 b 1…`
Payment:                          `0 3… 2 4 5 7 8 a d…d c` then `0 2 5 7 8 b 1`

| digit | wire | job |
|---|---|---|
| 4 | C0 `0RC` | front store empty: step over the empty cell (a filler over 0s, so any number of empty cells) |
| 5 7 | C1 D1 | the same two takes as the round, now on the payer |
| 8 | E0 `1LF` | give one cell, step left into a look |
| b | F1 `1LA` | look saw a 1: it was a round, go home as usual |
| a | F0 `1LG` | look saw a 0: it was a payment; join the block, go home as a different walker |
| d… | G1 `1LG` | filler: walk left over the old block |
| c | G0 `0LA` | at the far left: leave an empty cell; the old block is now the front store |
| 0 | A0 | the usual home digit now starts a new block |

Table: `1RB1LA_1RC1RB_0RC0RD_1RZ0LE_1LF---_1LG1LA_0LA1LG`
(13 wires used, digit 9 free, halt on digit 6).

Overlap used: the payer is paid by the round's own takes (5 7); the new
block is started by the round's own home digit (0). The payment costs only
4 new digits: 4, a, d, c.

Tested rule: block w, front store empty, payer d  →  new block 3, front
store w+2, payer d−2.  Example (9_ 4) → (3 11 2).

Tested runs: (3 4 4) halts after 11 home visits; (3 2 6) after 20;
(3 2 4 4) after 20. Reason: the landed store is w+2, and an odd store ends
in the number test (digit 6). So the odd/even of the block at each landing
decides life or halt. The test fires early on these tapes.

Not in this draft: the start from a blank tape (digit 4 walks right for ever
on an empty tape), the new row, and depth (empty cells are only stepped
over).
