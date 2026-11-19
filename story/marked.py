"""marked.py K [parts] [TURNS] : three counters, each with a mark that stays.  A counter of size c is c+1 cells of 1 (empty = a single 1).
   Tape  1^(c3+1) 0 1^(c2+1) 0 1^(c1+1) [0] 1^w ;  left of counter 3 the tape is blank.
   T  transfer     (.., c1, w)      -> (.., c1-1, w+K)
   B  borrow       (.., c2, 0, w)   -> (.., c2-1, w+2, 0)
   D  deep borrow  (c3, 0, 0, w)    -> (c3-1, w+3, 0, 0)        counter 1 is planted again as a single 1 at the far right
   H  halt         (0, 0, 0, w)     -> HALT                      all three empty: the head meets blank tape
   Z  boot         blank tape       -> (BOOT, 0, 0, 0)"""
import sys
K=int(sys.argv[1]);parts=sys.argv[2] if len(sys.argv)>2 else "TBDH";TURNS=int(sys.argv[3]) if len(sys.argv)>3 else 2;L=40;PAD=7
def conf(cs,w,start=PAD):
    cells=[0]*start
    for i,c in enumerate(cs): cells+=[1]*(c+1)+[0]
    head=len(cells)-1;cells+=[1]*w
    return cells,head
f=lambda c,h:"".join(("[%d]"%x) if i==h else str(x) for i,x in enumerate(c+[0]*(L-len(c))))
def emit(a,b,cap): print("S",f(*a),"S",f(*b),TURNS,cap)
if "T" in parts:
    for (cs,w) in [([1,1],0),([1,2],1),([2,1],2),([0,2],1),([1,3],3),([0,0,1],0)]:
        n=cs[:-1]+[cs[-1]-1]; emit(conf(cs,w),conf(n,w+K),2*(w+K)+12)
if "B" in parts:
    for (a,w) in [(1,1),(2,2),(1,3),(3,1),(2,0),(3,0)]:
        emit(conf([a,0],w),conf([a-1,w+2],0),2*w+16)
    emit(conf([0,1,0],2),conf([0,0,4],0),22)
if "D" in parts:
    for (a,w) in [(1,1),(2,2),(1,3),(3,1),(2,0)]:
        emit(conf([a,0,0],w),conf([a-1,w+3,0],0),2*w+22)
if "H" in parts:
    for w in [1,2,4]:
        c,h=conf([0,0,0],w);print("S",f(c,h),"HALT",TURNS,2*w+20)
if "Z" in parts:
    B=int(sys.argv[4]) if len(sys.argv)>4 else 2
    c,h=conf([B,0,0],0);blank=[0]*len(c)
    print("Y",f(blank,PAD),"S",f(c,h),3,60)
