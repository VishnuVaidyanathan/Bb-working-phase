"""quarters.py [TABLE ...] : how many wires of a table sit in each quarter.
   1st = writes 1, moves right; 2nd = writes 0, moves right; 3rd = writes 0, moves left; 4th = writes 1, moves left.
   Vishnu's hint for 7 states (24 Nov): 4 in the 1st, 3 in the 2nd, 2-3 in the 3rd, 3-4 in the 4th.  Thought tool only."""
import sys,re
def quarters(t):
    q=[0,0,0,0]
    for r in t.split("_"):
        for b in (0,1):
            e=r[b*3:b*3+3]
            if e[2] in "-Z" or e[0]=="-": continue
            q[{"1R":0,"0R":1,"0L":2,"1L":3}[e[:2]]]+=1
    return tuple(q)
def law(q): return q[0]==4 and q[1]==3 and q[2] in (2,3) and q[3] in (3,4)
if __name__=="__main__":
    for t in sys.argv[1:]: q=quarters(t);print(t,q,"fits" if law(q) else "does not fit")
