# Tables that look the same in the transcript, not in the TNF (23 Nov)

Vishnu's correction: a bigger machine is not "one or two wires near" Jeff
Ketchersid's table. It looks the same **in the transcript**. So the frame
must be written in transcript words, and the table is free inside it.

(For the record: the test of tables within two wire changes of Jeff's table
gave 57,214 tables, 517 of 533 survivors proved infinite by Quick_Sim, and
nothing bigger. Wrong kind of nearness.)

## The class (cls.c)

Every 7-state table with this grammar, as Vishnu read it from the transcript:
- the even digits make one closed loop A0→B0→C0→D0→E0→F0→A
  (A0 = `1RB`; the other five may write 0 or 1 and move L or R);
- the odd halves of the six loop states are three fillers (write 1, point to
  their own state), one take (write 0, points to its own state), one door
  (goes to G), one halt — in any arrangement, any directions;
- G is only behind the door; G0 and G1 are free and go back to the loop.

Tables are built only as far as a run from a blank tape needs them, so two
tables that behave the same are not counted twice.

Count (budget 3,000 steps while wires are still open):
- 18,977,338 full tables (every wire reached);
- 10,802,505 halt while a wire is still unchosen (small halters);
- 12,963,817 never reach some wire in 3,000 steps (loops and runaways).
Check: Jeff's table is in the set.

Running: all 18,977,338 from a blank tape.
