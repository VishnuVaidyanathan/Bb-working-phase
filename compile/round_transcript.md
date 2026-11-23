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
