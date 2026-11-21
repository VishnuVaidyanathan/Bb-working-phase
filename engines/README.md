# Engine sheet: which engine is the leanest?  (started 21 Nov)

Direction (Vishnu): everything is decided by the engine.  Before designing a 7- or 8-state machine with towers over towers, learn the
engines we know and measure them the same way.  One row per engine; every entry marked read by hand / tested / not known yet.

What is measured for each engine:
1. multiplier - what one unit of the payer does to the counter (n -> 2n+c, 3n+c, ...)
2. counts that go down, and by how much at a time (the stride)
3. the test on each count: zero test (a shape) or remainder test (a number)
4. rows of rows: does the result of a row become the length of the next row?
5. wires in use, and wires that do two jobs
6. first row from a blank tape (stores)

| Engine | States | Multiplier | Test | Rows of rows | First row | Wires free |
|---|---|---|---|---|---|---|
| Jeff Ketchersid, champion `1RB0RG_1RC1RB_0LD1RZ_0LE0LD_0LF1LE_1RA1LF_1LC0RB` | 7 | 3 | remainder, in twos (on the payers, and on the block at the row end) | yes: even block w -> new row of w/2, odd -> halt.  Real run: row of 3, then row of 22, then halt | 3, then 22 | 0 |
| Pavel Kropitz `1RB0RA_1LC1LF_1RD0LB_1RA1LE_1RZ0LC_1RG1LD_0RG0RF` | 7 | 2 | remainder, in threes; plus a fixed clock on the lead word | one row, then halt | 13 | 0 |
| holdout g4 `1RB0LG_1RC0RA_1LD1LE_1LB0LC_0LF0RE_0LG0LC_0RA---` (Polygon's list) | 7 | 2 | zero tests only (three levels) | yes, forever | 21 | 0 |
| our stack, 7 states `1RB1RG_1RC1RB_0LF0LD_1LC1LD_1LD0RB_0RA1LF_1RZ1RE` | 7 | round +3, stores of 2 | remainder in twos, blind (always even) | yes, forever | 424 | 0 |
| our stack, 8 states, round +2 stores of 3 | 8 | - | remainder in threes | one row, then halt | 14 | 0 |
| our stack, 10 states (engine A + boot) | 10 | round +4, stores of 3 | remainder in threes, class changes row to row | one short row, one tower-long row, then halt | 11 | 2 |

Gate rule seen in all of them: the stride of the test and the multiplier must share no divisor.
Not known yet: the wire cost of each job in Jeff's and Pavel's engines counted the same way as ours; whether any holdout has rows of rows
together with a multiplier of 3; what the leanest row-of-rows step costs.

Correction (21 Nov, night): the first version of this sheet said Jeff Ketchersid's engine is "one row, then halt".  Wrong.  Our own checked
rules (jeff/README.md) say his row end is a test in twos: block even -> a new row of half the block, block odd -> halt.  So his ENGINE has
rows of rows together with a number test, in 7 states.  His machine is small only because his start gives a first row of 3 stores; the row
made from it has 22.  Flowcharts of both machines in our terms: jeff_flowchart.*, pavel_flowchart.* (from the checked rules, not proved).

## Wires per job, counted the same way (21 Nov, night; observed)

| Job | Jeff Ketchersid's engine | Our stack (9-state engine A) |
|---|---|---|
| round (run, fill, look, eat, turn) | 9 wires | 9 wires |
| cutter | 4 wires (A1 G1 G0 F1), also used for the payment between depths and the start | 4 wires (A1 G1 H1 E1) + 1 runner (F1) |
| cut endings | 0 (the peel ends on the home wire or on the wire that starts the pairing) | 3 wires, used for nothing else |
| halt | 1 wire = the look the round makes at the gap | one of the 3 endings |
| total | 14 | 17 (+ boot) |
Lessons: (1) no wire should be only an ending; (2) the halt belongs on the round's look (the width of a gap), where a payer that pays
2 or 3 at a time is tested for free; (3) the second half of a cut can be done by the round's own wires.
