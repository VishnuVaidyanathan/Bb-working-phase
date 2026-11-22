# Two empty cells between stores: the frame "round and halt fixed, four wires free" (22 Nov)

Chosen by Vishnu (option 2), knowing it may end at Jeff Ketchersid's machine or near it.
Frame: in the two-empty-cell layout the grammar fixes the round (9 wires: A0 B0 B1 C0 D0 D1 E0 E1 F0) and the halt (C1, the look at
the gap).  Those ten wires are as in his table `1RB0RG_1RC1RB_0RD1RZ_0LE0LD_0LF1LE_1RA1LF_1LC0RB`.  The other four (A1, F1, G0, G1) do
the payment, the fresh stores, the new row and the start, so they set the free numbers.  All fills: 28^4 = 614,656 tables.

1. From a blank tape, 1,000,000 steps each (fam.c): 83,367 halt (none later than 100,000 steps), 531,289 run.  Of those running,
   83,591 lay 12 or more runs of 1s, but 81,038 of them never have a run longer than 3 (bouncers), 2,546 have runs of 4 to 19, and
   only 7 have a real block: his table, its twin (G0 = `0LD`, same behaviour), and 5 tables of one other family
   (A1=`1RF`, F1=`0LG`, G1=`1LF`), read by hand: a block that grows by 3 or 4 per visit with everything on one side - a bouncer.
2. Boot-free reading (fit.c): each table is put on four hand-made tapes in this layout - (7; 0 4 3), (6; 0 0 4 3), (9; 0 0 0 4 3),
   (7; 0 5 3) - and read at its next home visit.  Check on his table: (1; 12 2 3), (1; 2 9 2 3), (1; 2 2 10 2 3), (1; 12 3 3) =
   his checked rule (new block 1, landed = block + 7 - 2g, fresh stores of 2, payer - 2).
   Tables whose plain payment pays 2: FIVE, all with A1=`0RG`, F1=`1LF`, G1=`0RB`; only G0 differs:
     G0=`1LC` (his) and `0LD` (twin): new block 1, added 7
     G0=`0LB`: new block 2, added 6, fresh stores of 2, lands at the deepest empty level - a true cousin of the grammar
     G0=`0LG`: new block 1, added 6 at one level, but no fresh stores (the empty levels stay empty)
     G0=`0RD`: new block 4, landed 10, halts when two levels are empty
   The cousin G0=`0LB` from a blank tape, every start state: only a solid block that grows (58,824 cells after 1,000,000 steps);
   its row maker does not work.  Rows of rows from a blank tape: his machine only.
Result: inside this frame the grammar is realised by his table (and its twin) and by one cousin with no working start.  Three of the
four "free" wires are forced; the fourth has five workable values.  As foreseen, the frame leads back to his machine.
The useful by-product: fit.c judges an ENGINE without its start, in 30 microseconds a table (614,656 tables in 3 minutes).
