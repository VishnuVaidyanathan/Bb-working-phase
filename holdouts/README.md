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

## Gate test on the 70 deepest (gate_test.py, 21 Nov)

Test: rebuild the machine's own visits with every count shrunk to a small random number, 600 small tapes each; count how many halt.
Jeff Ketchersid's champion: 259 of 600 halt. Pavel Kropitz's champion: 466 of 600. Our own gateless 7-state stack: 59 (a gate its run never meets).
All 70 deepest holdouts: 0 of 600 each.
(A first version of the test rebuilt left-end tapes one cell off and wrongly reported 10 of them as gated; fixed, self check added.)

Read by hand (learn_any.py, tested on the real runs):
* family A, right end: m41/ - counters `10`, separators `100`; transfer a|b -> a-1|b+2; a lone counter becomes a fresh row. No halting rule.
* family A, left end: `1RB---_1RC1RA_0LD0LE_1RA0LE_0RF1LC_1RG1RA_1LE1RE` - the same rules in a mirror; its boot turns 11 into a row of 12.
* family B: `1RB1LA_0LC0RE_1LA1LD_1LC1LB_0LG0RF_1RD1RE_---0LF` - counters `10`, separators `1100`; the same transfer (a, b) -> (a-1, b+2);
  markers `110`, `1000`; a lone counter again becomes a short row of markers.
So the deep holdouts looked at are one idea in different clothes: a doubling stack with a boot and no reachable halt.
They most likely never halt (tested, not proved).

## Gate test on the other 641 (21 Nov)

200 small tapes each. 551 holdouts: none halt. 90 holdouts: at least one halts (most of them a handful; the two highest 149 and 113).
Of those 90, 21 also reach 3 or 4 arrows in the second tool before it runs out of time: results/gated_and_deep.txt.
They fall into two groups of cousins (a 3-arrow group and a 4-arrow group) plus one or two singles.
Status: tested, not proved. A halting small tape shows the table has a gate somewhere; it does not show the blank-tape run ever meets it.

## Sorting the gated holdouts by engine (22 Nov)

Aim: find a multiplying engine (block becomes store) that has rows of rows together with a number test.
Tried: Shawn Ligocki's Quick_Sim, 40 s each, on the 22 gated tower builders, the 35 number-gate holdouts and four engines we know
(Jeff Ketchersid's, Pavel Kropitz's, g4, our 7-state stack), reading which kinds of rules it proves.  The check failed: it reports
0 "Collatz rules" for Jeff's machine and 1 for our adding stack, so its labels do not sort engines the way we mean.  Not used.
What the run did show (none of the 61 halted):
* the 22 gated tower builders are two families: 10 with g4's rule profile (about (10^^^^)^9 reached) and 12 that all reach exactly
  (10^^^)^2 10^^3061;
* the 35 number-gate holdouts are all small (from 19-digit numbers up to (10^^)^238 10^^6).
One machine of the second family read by hand (lists.py, far-right turns in state D), `1RB0RG_1LC1LD_1LA0LB_0LE0RD_0LF0LB_0RG---_1RA1RA`:
    4  ->  1 | | | | |  ->  1 | | | # 2  -> ... ->  1 | # 8 # 2 -> 1 | # 7 | 3 | -> 1 | # 7 | | 6 -> 1 | # 7 # 8 -> 1 | # 6 | 9 | -> ... -> 1 | # 6 # 20 -> ... 44
Same words (`10`, `100`, `1000`) and the same rules as g4:  k # n # -> k-1 | n+1 | -> k-1 | | 2n+2 -> k-1 # 2n+4,  lone M -> row of M+1 bars.
It is g4's engine in another table, with a first row of 5 bars instead of 21 (observed on one machine; the other 11 not read).
So the gated tower builders in Polygon's list show ONE engine: the doubling stack with zero tests only.  No holdout read so far has
rows of rows together with a number test.

## Re-screen of all 711 holdouts by rule levels (22 Nov), after prurq's analysis of TM 721

prurq (Discord Busy Beaver community) showed that `1RB0LD_0LC0RA_1RE1LD_1LE1RF_1LF0RC_1RG0LE_---1RA` has an arrow mechanism ("overflow")
and said it is surely not the only one in the list.  Our earlier code for that machine ("small growth") was wrong: Quick_Sim had run
out of memory with blocks of 2.  So every holdout was run again through Shawn Ligocki's Quick_Sim (our wrapper, memory capped at 3 GB,
15 s each), recording the highest rule level it proves.  First pass: for 344 machines the level lines were cut off by our own script
(only the end of the output was kept); those were run again with the whole output kept.  None of the 711 halted.
Highest level proved:   0: 3    1: 41    2: 161    3: 188    4: 57    5: 136    6: 55    7: 1    8: 16    9: 51    10: 2
So 261 holdouts reach level 5 or more in 15 seconds and 69 reach level 8 to 10: the arrow mechanism is common in the list, as prurq said.
(The list itself stays out of this repo; only counts are given.)
Joined with our older small-tape test (how many tiny tapes halt after more than 1,000 steps): none of the 261 shows such a late halt;
the 35 machines that do are all at level 0 to 4.  That older test is weak: it also shows nothing for TM 721, whose halt (second counter
odd, third even) we found today on a purpose-made grid.  So "no number test among the arrow machines" is NOT established.

## Reading the arrow machines (22 Nov): what their engines are

The 69 holdouts at level 8 to 10 fall into about 36 families (within 3 wires of each other): many different tables.
The deepest, `1RB1LA_0LC0RE_1LA1LD_1LC1LB_0LG0RF_1RD1RE_---0LF` (level 10), read by hand at its far-right turns:
    1.2 (1.1)^4 2.2 (1.1)^3 2.2 (1.1)^8  ->  ... (1.1)^2 2.2 (1.1)^10 ...  ->  1.2 (1.1)^4 (2.2)^2 (1.1)^7  ->  1.2 (1.1)^4 3.2 (1.1)^11  ->  1.2 (1.1)^3 2.2 (1.1)^10 ...
Counters of `10` words kept apart by `1100` markers; the middle counter pays 1, the last gains 2; when the middle one is empty two
markers join and the counter to the left pays 1.  The grammar of g4 (a doubling stack that pays in ones) in another table.
transfer.py reads the commonest transfer of a machine (checked on Jeff Ketchersid's: pay 1 gain 3; Pavel Kropitz's and g4: pay 1
gain 2; TM 721: pay 2 gain 4; our from-scratch machine: pay 2 gain 3).  It reads the round only, not a deeper payment.
On the 261 arrow machines (level 5 or more), 300,000 steps each:
    256  words, pay 1, gain 2      (doubling stacks)
      1  words, pay 1, gain 3      (a tripling stack)
      2  words, pay 1, gain 1
      2  no transfer seen
So almost every arrow machine in the list is the same engine: the doubling stack with zero tests.  By the gate rule none of those has
a number test in its round.
The one that triples, `1RB1RC_0LC0LE_1RA1LD_1LB1RB_1RF1LB_0RF0RG_0RA---`, read by hand: a block of 17 is cut into 8 bars (2 cells per bar)
with 1 left over; then on the left `(1.1)^4 | (1.1)^4` -> `(1.1)^7 | (1.1)^3` -> `(1.1)^10 | (1.1)^2` ... pay 1, gain 3; bars are
taken from the row one at a time.  That is Jeff Ketchersid's grammar (triple, rows cut in twos) in the WORD layout.  Quick_Sim, 100 s:
no halt, level 6, about (10^^^^^)^31 and climbing, with tower heights near 26,150,88x,xxx.  Its row has 8 bars, so it would be smaller
than his machine (22 stores) even if it halts.  Whether it halts: not known.

Correction (22 Nov, later): the tripling machine does NOT cut its rows in twos; read in full in
holdouts/read/1RB1RC_0LC0LE_1RA1LD_1LB1RB_1RF1LB_0RF0RG_0RA---.md.  It pays in ones everywhere.  So none of the 261 arrow machines read
so far shows a payment other than 1 in its round.

## The other 450 holdouts read with transfer.py (22 Nov, night): not all doubling stacks

Asked: is a machine a little bigger than Jeff Ketchersid's sitting among the holdouts?  Such a machine would show few rule levels in a
short Quick_Sim run, so the 450 holdouts below level 5 were read too (300,000 steps each; commonest transfer; the round only).
    words, pay 1 gain 2: 372      no transfer seen: 23      words, pay 1 gain 3: 6      words, pay 3 gain 9: 4
    solid, pay 2 gain 6: 7 (seen only twice each - weak)     solid, pay 1 gain 2: 5      solid, pay 198 gain 237: 5 (not a round)
    solid, pay 2 gain 4: 2 (one is TM 721)     solid, pay 2 gain 3: 2     solid, pay 1 gain 3: 2     solid, pay 3 gain 6: 2
    solid, pay 1 gain 6: 3     and 17 others, one or two machines each
Where the gain per unit paid and the payment share no divisor (gate rule met, on the round alone):
    solid, pay 3 gain 6 (x2 against threes): 2 machines, seen about 900 times each - the numbers of Pavel Kropitz's engine on solid counters
    solid, pay 1 gain 3: 2 machines (the round of Jeff Ketchersid's engine; a deeper payment is not shown by this tool)
    solid, pay 2 gain 6 (x3 against twos): 7 machines, weakly seen
The "pay 2 gain 3" reading was wrong for the one machine read by hand so far,
`1RB1RA_1LB1RC_0RG0LD_0RF1LE_1LA1LD_---0RB_0RA0RF` (run lengths at the far-left blank cell):
    4 6 12 -> 4 10 10 -> 4 14 8 -> ... -> 4 30 -> 2 33 -> 4 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2_ 3      and earlier  4 10_ 1 -> 2 13_ 1 -> 4 2 14
Solid counters one cell apart; a counter pays 2 and its neighbour gains 4 (the tool caught a half-step); a used-up level gets a fresh
store of 2 with the landed number behind it; a lone 33 becomes a ROW of 16 stores of 2 and a 3: rows cut in twos, in the one-cell
layout.  Multiplier 2 with payments of 2: nothing changes in twos, so no number test is fed (same reason as TM 721).  Not known to halt.
Not read by hand yet: the two "pay 3 gain 6" machines, the two "pay 1 gain 3", the seven "pay 2 gain 6".

## Three more read by hand (22 Nov, night): the transfer tool misleads; one true coin machine, of a small kind

* the two "solid, pay 1 gain 3" machines (`1RB0LF_0LC1RE_1RG1LD_0RB1LF_1RB1LA_1LE1LC_---0RC` and its renamed twin): not his round.
  7 6 2 2 -> ... unit cells are laid in front two at a time while a counter pays 2, then they join: 7 -> 19 (about 2b+5), with a few
  small stores behind (3 2 2).  A doubling machine with little depth; Quick_Sim: level 1, about 10^3,800.  The tool had caught a half-step.
* `1RB1RA_1LC0LF_1LE1LD_1LC0RE_1LF0LB_0RA1RG_0RD---` ("solid, pay 3 gain 6"): read at the far-left blank cell:
    4 9 -> 10 6 -> 16 3 -> 22 -> 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 -> 5 1.. -> 13 1.. -> 4 10 1.. -> 10 7 -> 16 4 -> 22 1 -> 29 1.. -> 37 1..
  A counter pays 3 and the block gains 6 (it doubles, against a payment in threes: gate rule met); a lone 22 becomes a ROW of 15
  one-cell stores; the row is used a couple of stores at a time.
  Grid of small tapes, head in state F at the far-left blank: (4, b) for b = 1..15: only b = 2 halts (at step 22).
  (4, b, 1, 1, 1): b = 4 halts at step 15,143 and b = 10 at step 16,721; the other 13 run on.  (4, b, six 1s): none halts in 400,000 steps.
  So it has a halt that depends on a number and fires late: a number test that IS fed.
  Real run: direct, 30,000,000,000 steps, no halt, 295,557 ones, longest run 196,594.  Quick_Sim, 100 s: no halt, level 1,
  about 10^57,291, and it reports one "Collatz rule".
  Kind: each row gives about one doubling per store, so a row of n stores gives roughly 2^(n/2); the next row is about two thirds of
  that.  One exponential per ROW - a tower as tall as the number of rows it survives.  That is far below one arrow per STORE
  (Jeff Ketchersid's 22-store row).  If its test fails after a few rows it halts small; whether it ever fails is not known.
  It is the first holdout we have read whose halt is a real coin - and it shows that a coin on a slow engine does not give a big machine.
* one of the seven "solid, pay 2 gain 6" machines, `1RB0LD_0RC1RG_1LD1RF_1LE1LC_0LA0RA_0RA0LA_0RA---`: single cells kept apart by 2 or 3
  empty cells, with a small counter (5, 3, 1) walking through them; Quick_Sim level 2, about 10^^4.  Not a tripling stack; the tool's
  reading came from two chance matches.
So far no holdout read has his grammar with a longer full row.  transfer.py is a pointer, not a reading: every hit must be read by hand.
