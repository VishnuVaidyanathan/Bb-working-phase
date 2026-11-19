"""gate3.py [parts]: two marked counters, a tower, and a gate on the working block modulo 3.
   Tape  1^(c2+1) 0 1^(c1+1) [0] 1^w , blank to the left.
   T transfer (c2, c1, w) -> (c2, c1-1, w+2)        B borrow (c2, 0, w) -> (c2-1, w+2, 0)
   G tower    (0, 0, w), w = 0 mod 3 -> (w+3, 0, 0) H halt   (0, 0, w), w = 1 mod 3 -> HALT
   Z boot     blank -> (2, 0, 0)"""
import sys
parts=sys.argv[1] if len(sys.argv)>1 else "TBGH";TURNS=2;L=40;PAD=7
def conf(cs,w,start=PAD):
    cells=[0]*start
    for c in cs: cells+=[1]*(c+1)+[0]
    head=len(cells)-1;cells+=[1]*w
    return cells,head
f=lambda c,h:"".join(("[%d]"%x) if i==h else str(x) for i,x in enumerate(c+[0]*(L-len(c))))
def emit(a,b,cap,v="S",t=TURNS): print(v,f(*a),"S",f(*b),t,cap)
if "T" in parts:
    for (cs,w) in [([1,1],0),([1,2],1),([2,1],2),([0,2],1),([1,3],3)]: emit(conf(cs,w),conf([cs[0],cs[1]-1],w+2),2*(w+2)+12)
if "B" in parts:
    for (a,w) in [(1,1),(2,2),(1,3),(3,1),(2,0),(3,0)]: emit(conf([a,0],w),conf([a-1,w+2],0),2*w+16)
if "G" in parts:
    for w in [3,6,9]: emit(conf([0,0],w),conf([w+3,0],0),2*w+22)
if "H" in parts:
    for w in [1,4,7]:
        c,h=conf([0,0],w);print("S",f(c,h),"HALT",TURNS,2*w+20)
if "Z" in parts:
    c,h=conf([2,0],0);print("Y",f([0]*len(c),PAD+3),"S",f(c,h),3,40)
