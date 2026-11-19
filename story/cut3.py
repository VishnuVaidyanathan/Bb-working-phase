"""cut3.py : the cut-by-3 story as arithmetic.  Layer (k, m): block B = k + m(3+E) + 5 (B = 4 at the blank start).
   q, r = divmod(B-1, 3).  r=0: next layer (0, q).  r=1: next layer (E+1, q).  r=2: halt."""
import math,sys
def fate(E,maxl=3000):
    k=m=0;steps=0
    for L in range(1,maxl+1):
        B=(4 if L==1 else k+m*(3+E)+5);q,r=divmod(B-1,3)
        steps+=(3+E)*m*m+2*k*m+3*B
        if r==2: return L,B,steps
        k,m=(0,q) if r==0 else (E+1,q)
    return None
if __name__=="__main__":
    for E in range(1,41):
        f=fate(E);b=lambda x:("%d"%x) if x<10**9 else "10^%.1f"%math.log10(x)
        print("E=%2d  x%d/3 "%(E,3+E),("halts in layer %3d   ones %s   steps about %s"%(f[0],b(f[1]),b(f[2]))) if f else "no halt in 3000 layers")
