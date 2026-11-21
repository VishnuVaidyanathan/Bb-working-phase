# holdouts : 7-state tables nobody has decided yet

The list studied here: 711 seven-state tables, each with one open cell (`---` = halt if reached). The list itself is not kept in this repo.
Source: Polygon, Discord Busy Beaver community ("1266 toplevel TMs, run 25, holdouts"), passed on by Vishnu on 21 Nov 2026.
The list is Polygon's work; only our results on it are recorded here.

What we did with it:
* 20 million steps each from a blank tape, tape read as stores (design/hand.c): none halts; about 560 tapes are rows of the word `10`
  (the coding Pavel Kropitz's machine uses), about 100 are rows of 2s, 12 show a big store with a row of equal stores behind it.
* Quick_Sim (Shawn Ligocki) with our remainder calculator (calc/), 17 seconds each: results to be added.

## Results on the 711 (21 Nov 2026; Quick_Sim by Shawn Ligocki + calc/, tested as far as the run times go)

First pass, 17 seconds each: 0 halted, 0 proved infinite, 33 stopped on a simulator error (fixed later, see calc/README.md), 10 used the
remainder calculator.  Arrows reached: 10 (1 table), 9 (13), 8 (53), 7 (3), 5 (44), 4 (116), 3 (84), 2 (237), 1 or none (160).

The 70 at 7 arrows or more, 190 seconds each: 0 halted, 0 proved infinite, 0 errors, 0 remainders needed; reached 10 (6 tables), 9 (22), 8 (33).
One more arrow costs the simulator about ten times the time.

The 33 that had stopped on the error, 190 seconds each with the fix: 0 halted, 0 proved infinite; reached 5 arrows (17), 4 (15), 2 (1);
one stops on a different simulator assertion.

The 10 that used the remainder calculator are all of the form (10^^)^k: a tower step repeated k times, with one remainder asked per step
(29 to 245 remainders in 17 seconds, all passed).  Even if one of these halts, it is a 3-arrow number.

Read by hand: m41/ (a row of 46, no gate, most likely never halts).
No table in this list has been shown to halt, and none has been shown to be bigger than the champion.
