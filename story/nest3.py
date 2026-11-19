"""nest3.py K [parts] [TURNS]: our own story with three counters.  Tape  1^c3 0 1^c2 0 1^c1 [0] 1^w  (an empty counter is nothing: two 0s touch).
   T   transfer        (.., c1, w)       -> (.., c1-1, w+K)
   B   borrow          (.., c2, 0, w)    -> (.., c2-1, w+2, 0)          the working block becomes counter 1
   D   deep borrow     (c3, 0, 0, w)     -> (c3-1, w+3, 0, 0)           the working block becomes counter 2, counter 1 stays as an empty place
   H   halt            (0, 0, 0, w)      -> HALT
   Z   boot            blank, start state -> (BOOT, 0, 0, 1)"""
import sys
K=int(sys.argv[1]);parts=sys.argv[2] if len(sys.argv)>2 else "TBDH";TURNS=int(sys.argv[3]) if len(sys.argv)>3 else 2;L=36;PAD=7
def conf(blocks,w,extra=0):
    cells=[0]*PAD
    for i,c in enumerate(blocks): cells+=[1]*c+([0] if i<len(blocks)-1 else [])
    cells+=[0]*extra;head=len(cells);cells+=[0]+[1]*w
    return cells,head
f=lambda c,h:"".join(("[%d]"%x) if i==h else str(x) for i,x in enumerate(c+[0]*(L-len(c))))
def emit(a,b,cap,v="S"): print(v,f(*a),"S",f(*b),TURNS,cap)
if "T" in parts:
    for (a,b,w) in [(1,1,0),(1,2,1),(2,1,2),(0,2,1),(1,3,3),(2,2,0)]: emit(conf([a,b],w),conf([a,b-1],w+K),2*(w+K)+12)
if "B" in parts:
    for (a,w) in [(1,1),(2,2),(1,3),(3,1),(2,4),(2,0),(3,0)]: emit(conf([a,0],w),conf([a-1,w+2],0),2*w+14)
if "D" in parts:
    for (a,w) in [(1,1),(2,2),(1,3),(3,1),(2,0)]:
        c1,h1=conf([a,0,0],w);c2,h2=conf([a-1,w+3],0,extra=1); emit((c1,h1),(c2,h2),2*w+18)
if "H" in parts:
    for w in [1,2,4]:
        c,h=conf([0,0,0],w);print("S",f(c,h),"HALT",TURNS,2*w+16)
