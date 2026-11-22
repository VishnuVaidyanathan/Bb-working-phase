# Can an overflow machine be made to halt?  First try: the neighbours of TM 721 (22 Nov)

TM 721 = `1RB0LD_0LC0RA_1RE1LD_1LE1RF_1LF0RC_1RG0LE_---1RA` (Polygon's list; analysed by prurq, see holdouts/read/).  "Overflow" is
prurq's word for a lone counter turning into a run of `1110` blocks, each block worth one arrow (our "rows of rows").

1. TM 721 already has a number test.  ovf.c puts a table, without its start, on hand-made tapes (3 b c), b = 3..10, c = 1..6
   (head in state D on the blank cell left of the first run), 60,000 steps each.  TM 721 halts exactly when b is odd and c is even,
   and after real work; every other tape runs on.  In its real run c is always odd, so the test is never fed (prurq's conjecture that
   the rules keep things the same in twos; our gate rule: multiplier 2, payments of 2).
   So the task is not to add a test but to change the arithmetic.  With a multiplier of 2 a changed constant can only make c always
   odd or even at the first refill; a halt after several overflows needs an odd multiplier.
2. Every table within two wire changes (halt wire kept): 57,214.  Overflow kept (tape (3 3 3) shows 20 or more runs within 400,000
   steps): 12,725.  Of those: 11,871 never halt on the grid, 5 halt everywhere, 849 are mixed.  Some mixed patterns go in threes,
   not twos (39 tables with one such pattern) - not read by hand.
3. The 755 tables with overflow kept and a clearly mixed grid (6 or more tapes halting, 6 or more running), from a blank tape,
   300,000,000 steps: 106 halt before 100,000 steps, 236 run off an 8-million-cell tape, 413 still running; halting late: 0.
   Of the 413: 254 never show a run longer than 99 cells (bouncers), 158 show a block of 5,000 cells or more, 1 other.
4. Those 158 through Shawn Ligocki's Quick_Sim, block size 4, 20 s each (run through calc/quick_sim_with_remainders.py):
   147 shown never to halt (rule level 1 or 2), 10 not settled at level 1, and one reaching level 4: TM 721 itself.
Result: within two wire changes, the only arrow machine among the candidates is TM 721.  No halting overflow machine found.
Not looked at: the 11,871 tables that keep the overflow and never halt on the grid (they have no test on these tapes), and the
94 mixed tables below the "6 and 6" bar.
