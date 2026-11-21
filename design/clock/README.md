# Clock test and the fill of a Pavel-style skeleton (21 Nov)

Idea: size is counted in rows. One row then halt (Jeff Ketchersid 22, Pavel Kropitz 13) gives about "row - 2" arrows.
A machine that makes a second row from the result of the first, and then halts, would be past every one-row machine.

clock.c: finds a visit "lead word + one lone counter" in the machine's own run, then follows small tapes of that form tick by tick
(H halt, R a row starts, g grows and comes back).  Pavel's table reads "R H"; the row-of-21 holdout reads "R R R ..." (never H).

Skeleton filled: `1RB???_1LC1LF_???0LB_???1LE_---0LC_???1LD_??????` (Pavel's chain of five wires over ones, his halt, his left pusher; six wires open).
Result (tested): 1,536,260 fillings use every wire; 67,316 reach a lone-counter visit; the clock test passes 1,214 (991 "one row", 223 "two or more").
Shawn Ligocki's Quick_Sim, 20 s each, on the 1,214: all but about 100 are proved never to halt; the rest are slow growers or one-arrow counters;
exactly one builds a deep tower, and it is Pavel's own table.  New machines: 0.
Weakness of the test found on the way: "R" only shows a row starts; in the failed tables the "row" never ends.
