"""frame5.py : every table in the frame "hand round of five + halt outside" (23 Nov, Vishnu's question:
   with the halt outside, can pay and lay be built within the two states behind the door?).
   Fixed (the hand round, tested): A0 1RB, B0 1RC, B1 1RB, C0 0RD, D0 0LE, D1 0LD, E0 1LA, E1 1LE; C1 = halt.
   Open: the door A1 (any write, any move, goes to F) and all four wires of F and G (any write, move, state).
   4 * 28^4 = 2,458,624 tables, one per line.  Thought tool only."""
import itertools,sys
opts=[w+m+s for w in "01" for m in "LR" for s in "ABCDEFG"]
out=sys.stdout.write
for a1 in ("0LF","0RF","1LF","1RF"):
    for f0 in opts:
        for f1 in opts:
            for g0 in opts:
                pre="1RB%s_1RC1RB_0RD1RZ_0LE0LD_1LA1LE_%s%s_%s"%(a1,f0,f1,g0)
                out("".join(pre+g1+"\n" for g1 in opts))
