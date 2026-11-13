# BB working phase

Working notes and programs for Busy Beaver work that is still in progress.
Author: Vishnu Vaidyanathan (independent researcher).
The finished BB(5) work is in the separate repository
`BB5-decimal-macrogrammar`; this repository is for the rest.

Everything here uses the same lens: one digit per step,
`digit = 2*state + symbol`, and the run is read as a grammar of those digits.

| Folder | What is in it | Status |
| --- | --- | --- |
| [`bb7/`](bb7) | The claimed BB(7) champion (Jeff Ketchersid's machine): its transcript grammar, a check that the grammar is closed, the halting induction on paper, and a Coq proof that it halts from a blank tape. | Halting proved in Coq (no axioms). The score and the bound are not in our Coq. |
| [`bb7/design/`](bb7/design) | The try at designing a bigger BB(7) machine from parts: loops, doors, fuel, gate, boot, swap, the oscillator reading, wire jobs, and the cousin searches. Every step is written down, including the ones that failed. | No machine bigger than the champion. No cousin except its twin. |
| [`cousins/`](cousins) | Building cousins of a champion from its grammar roles, tested on BB(5). | Works for BB(5): gives the champion and 13 known top halters, nothing else. Not expected to carry to BB(7). |

## Prior work on the BB(7) machine

- Jeff Ketchersid found the machine, and his repository
  `jeff87654/busy-beaver` has a Coq proof of halting, the score and the bound.
- `CasimirKnights/BeaverNumbers` (Lean 4) gives a step count and score.

Our Coq proof of halting was written independently and is the third.
The BB(6) rules used along the way are by mxdys.

## Rule used in the design notes

A machine counts only if it is run from a blank tape. Parts found on prepared
tapes are parts, not machines.
