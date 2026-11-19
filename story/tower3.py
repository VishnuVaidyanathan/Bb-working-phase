"""tower3.py K [parts] : my own story "counter, ticket block, working block", head resting between the last two.
   Tape  1^a 0 1^b [0] 1^w .
   T  transfer : (a, b, w) -> (a, b-1, w+K)      the wall steps left; K-1 new cells at the far right
   B  borrow   : (a, 0, w) -> (a-1, w+2, 0)      a pays one cell; the whole working block becomes the ticket block
   G  tower    : (0, 0, w) -> (w, 1, 1)          the working block becomes the counter; plant 0 1 0 1 after it
   parts: letters from TBG (default all).  Prints loose pictures."""
import sys
TURNS=2
K=int(sys.argv[1]);parts=sys.argv[2] if len(sys.argv)>2 else "TBG";L=34;PAD=6
def conf(a,b,w,shift=0):
    cells=[0]*(PAD+shift)+[1]*a+[0]+[1]*b;head=len(cells);cells+=[0]+[1]*w
    return cells,head
def emit(c1,h1,c2,h2,turns,cap):
    f=lambda c,h:"".join(("[%d]"%x) if i==h else str(x) for i,x in enumerate(c+[0]*(L-len(c))))
    print("S",f(c1,h1),"S",f(c2,h2),turns,cap)
if "T" in parts:
    for (a,b,w) in [(1,1,0),(1,2,1),(2,1,2),(0,2,1),(1,3,3),(2,2,0)]:
        c1,h1=conf(a,b,w);c2,h2=conf(a,b-1,w+K)
        emit(c1,h1,c2,h2,TURNS,2*(w+K)+12)
if "B" in parts:
    for (a,w) in [(1,1),(2,2),(1,3),(3,1),(2,4)]:
        c1,h1=conf(a,0,w);c2,h2=conf(a-1,w+2,0)
        emit(c1,h1,c2,h2,TURNS,2*w+14)
if "G" in parts:
    for w in [2,3,4]:
        c1,h1=conf(0,0,w);c2,h2=conf(w,1,1,shift=2)
        emit(c1,h1,c2,h2,TURNS,2*w+14)
