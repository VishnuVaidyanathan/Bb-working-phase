# Road signatures

For each machine, run from a blank tape for 3,000,000 steps (none of the 7-state ones halts in that time).
A road is a pair of digits that follow each other in the run. Rare roads that first appear later are not counted.

- **before: one / two / three+**: digits that are reached from one, two, or three or more different digits
- **after: one**: digits that always go to the same next digit
- **pipes**: one digit before and one digit after
- **one-wire loops**: digits that follow themselves (a walk)
- **halt**: the halting digit, and the digits whose state change leads into its state

Made with `tools/signature.py`. J = Jeff Ketchersid's machine, P = Pavel Kropitz's, D1 = Andrew Ducharme's 4-arrow machine, N1 = `1RB0RE_0RC0RG_1LD0LE_1RA1LA_1LC0LF_1LD1RZ_1RA1RB` from the group's top-20 list; the other labels are as in `catalogue.md`.

| label | states | wires | roads | before: one | two | three+ | after: one | pipes | one-wire loops | halt |
|---|---|---|---|---|---|---|---|---|---|---|
| J2 | 7 | 13 | 23 | 0147cd | 89ab | 236 | 27c | 7c | 39b | 5 after 2 | |
| D1 | 7 | 13 | 24 | 234abd | 015 | 6789 | 24 | 24 | - | c after 4 | |
| Q1 | 7 | 13 | 22 | 0128abd | 679c | 54 | 012a | 012a | 5 | 3 after 0 | |
| D2 | 7 | 13 | 24 | 89cd | 012345a | 67 | 8c | 8c | 16 | b after 8c | |
| D3 | 7 | 13 | 22 | 1234a | 05678cd | 9 | 1238 | 123 | 579c | b after 8 | |
| D4 | 7 | 13 | 23 | 25abcd | 4689 | 017 | 04c | c | - | 3 after 0 | |
| D5 | 7 | 13 | 24 | 17cd | 02389ab | 45 | 13 | 1 | 9 | 6 after 1 | |
| D6 | 7 | 13 | 24 | 2367d | 019ab | 458 | 68 | 6 | - | c after 8 | |
| D7 | 7 | 13 | 24 | 57cd | 01489ab | 23 | 15 | 5 | 9 | 6 after 5 | |
| D8 | 7 | 13 | 22 | 14567b | 039cd | 28 | 1479 | 147 | - | a after 1 | |
| D9 | 7 | 13 | 22 | 123abc | 04789 | 56 | 128c | 12c | - | d after 1 | |
| T286 | 7 | 13 | 25 | 0123c | 6789 | 45ab | 3 | 3 | 7 | d after 3 | |
| T246 | 7 | 13 | 24 | 23abd | 45789 | 016 | bd | bd | 57 | c after b | |
| T140 | 7 | 13 | 23 | 6abd | 01235789 | 4 | 68d | 6d | - | c after 6 | |
| T93 | 7 | 13 | 21 | 23456ad | 18bc | 09 | 146ad | 46ad | - | 7 after 4 | |
| T46 | 7 | 13 | 21 | 0146cd | 2789ab | 3 | 124ad | 14d | - | 5 after 2 | |
| T35 | 7 | 13 | 21 | 239bcd | 01467a | 5 | 367ac | 3c | 1 | 8 after 7 | |
| T22 | 7 | 13 | 21 | 4569abd | 0178 | 23 | 49abd | 49abd | 7 | c after a | |
| W5 | 7 | 12 | 21 | 4569 | 37cd | 2ab | 047 | 4 | - | 8 after 7 | |
| S5 | 6 | 11 | 20 | 1b | 023456789 | - | 13 | 1 | 58 | a after 3 | |
| J | 7 | 13 | 23 | 017cd | 4689ab | 23 | 27c | 7c | 39b | 5 after 2c | |
| P | 7 | 13 | 22 | 079c | 123456abd | - | 67bc | 7c | 1 | 8 after 7 | |
| T15 | 6 | 11 | 19 | 016b | 23589a | 4 | 128 | 1 | 4 | 7 after 1 | |
| S6 | 6 | 11 | 19 | 26ab | 145789 | 0 | 046 | 6 | 1 | 3 after 0 | |
| N1 | 7 | 13 | 24 | acd | 023456789 | 1 | 69 | - | - | b after 9 | |
| BB5 | 5 | 9 | 16 | 59 | 0123467 | - | 25 | 5 | 37 | 8 after 5 | |

## What it shows

- 7-state machines use 21 to 25 of the 26 roads a table allows. Jeff's uses 23, Pavel's 22.
- Jeff's machine has two digits fed by three others (2 and 3, both state B, the walk right). Pavel's has none. Andrew Ducharme's has four. So a triple junction is not a common law of deep machines.
- Digits 7 and c are pure pipes in both Jeff's and Pavel's machines.
- No simple count in this table separates the deep machines from the shallow ones.
