# BB working phase

Working notes and programs for Busy Beaver work that is still in progress.
Author: Vishnu Vaidyanathan (independent researcher).
The finished BB(5) work is in the separate repository
`BB5-decimal-macrogrammar`; this repository is for the rest.

Everything here uses the same lens: one digit per step,
`digit = 2*state + symbol`, and the run is read as a grammar of those digits.

| Folder | What is in it | Status |
| --- | --- | --- |
| [`START_HERE.md`](START_HERE.md) | Where the work stands and how to resume it. | Kept up to date. |
| [`bb7/`](bb7) | The claimed BB(7) champion (Jeff Ketchersid's machine): its transcript grammar, the halting induction on paper, and a Coq proof that it halts from a blank tape. | Halting proved in Coq (no axioms). The score and the bound are not in our Coq. |
| [`bb7/boot/`](bb7/boot) | The champion's boot written by hand from the words of the big run, and the small-size table. | 319 of 319 digits match. |
| [`bb7/gate_notes.md`](bb7/gate_notes.md) | The opening and the parity gate of the champion. | Tested; the halting part is proved. |
| [`bb7/transcript_to_table/`](bb7/transcript_to_table) | Tools that go from a written transcript to the tables that can play it. | Working. |
| [`bb7/design/`](bb7/design) | The earlier try at designing a bigger BB(7) machine from parts. Every step is written down, including the ones that failed. | No machine bigger than the champion. |
| [`story/`](story) | From a tape story to a table: draw the tape at every head turn, and the tool finds the tables that play it. | Working. Finds the BB(5) champion from pictures alone. No big new machine yet. |
| [`flow/`](flow) | Wiring first: fix which state each digit flows to, try every write and move, keep the tables that fit the recipe in digits. | Working. Picks Pavel's machine out of 29,152. No new deep machine yet. |
| [`cousins/`](cousins) | Building cousins of a champion from its grammar roles, tested on BB(5). | Works for BB(5). |
| [`cousins/bb7/`](cousins/bb7) | The same search for the BB(7) champion: lower cousins, halting cousins found with Quick_Sim, and what is still open. | Nothing bigger than the champion. |
| [`cousins/bb7/base4/`](cousins/bb7/base4) | A base-4 tower machine from that search, with a Coq proof that it never halts. | Proved in Coq (no axioms). |
| [`study/`](study) | Big machines read side by side: a five-machine comparison, a catalogue of 24, a 4-arrow machine read in full, which wires do more than one job, and two families of "late wires freed". | Reading notes; each statement is marked proved, tested or observed. |

## Prior work on the BB(7) machine

- Jeff Ketchersid found the machine, and his repository
  `jeff87654/busy-beaver` has a Coq proof of halting, the score and the bound.
- `CasimirKnights/BeaverNumbers` (Lean 4) gives a step count and score.

Our Coq proof of halting was written independently and is the third.
The BB(6) rules used along the way are by mxdys.
The simulator used in `cousins/bb7/` and `study/` is Shawn Ligocki's Quick_Sim (`sligocki/busy-beaver`).
The other machines in `study/` are by Pavel Kropitz and Andrew Ducharme, as listed on the bbchallenge wiki.

## Rule used in the design notes

A machine counts only if it is run from a blank tape. Parts found on prepared
tapes are parts, not machines.
