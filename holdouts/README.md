# holdouts : 7-state tables nobody has decided yet

The list studied here: 711 seven-state tables, each with one open cell (`---` = halt if reached). The list itself is not kept in this repo.
Source: Polygon, Discord Busy Beaver community ("1266 toplevel TMs, run 25, holdouts"), passed on by Vishnu on 21 Nov 2026.
The list is Polygon's work; only our results on it are recorded here.

What we did with it:
* 20 million steps each from a blank tape, tape read as stores (design/hand.c): none halts; about 560 tapes are rows of the word `10`
  (the coding Pavel Kropitz's machine uses), about 100 are rows of 2s, 12 show a big store with a row of equal stores behind it.
* Quick_Sim (Shawn Ligocki) with our remainder calculator (calc/), 17 seconds each: results to be added.
