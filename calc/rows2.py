"""rows2.py : the power test, row after row.  For a stack design (round +K, fresh store m) a cut row is: block m, then n-1 stores of m,
   then a last store r (the leftover, 0 = none).  When that row is used up the block is W; the next cut has leftover (W + K) mod m.
   This lists that leftover for n = 2..NMAX, to see whether it settles as rows get long (a tower-long row then has the settled value).
   Exact remainders by remainder.py.   Usage: python3 rows2.py [NMAX]"""
import sys,signal
import stackcalc as S
import remainder as R
class TO(Exception): pass
def alarm(*a): raise TO()
signal.signal(signal.SIGALRM,alarm)
NMAX=int(sys.argv[1]) if len(sys.argv)>1 else 7
for K in range(1,8):
    for m in range(2,6):
        D=S.Design(K,m);line=[]
        for r in range(0,m):
            out=[]
            for n in range(2,NMAX+1):
                stores=[m]*(n-1)+([r] if r else [])
                try:
                    signal.alarm(20);f=D.row_end(m,stores);v=(R.mod_(f,m,{})+K)%m;signal.alarm(0);out.append(str(v))
                except TO: out.append("?");break
                except Exception as e: signal.alarm(0);out.append("x");break
            line.append("last store %d: %s"%(r," ".join(out)))
        print("round +%d store %d | "%(K,m)+" | ".join(line),flush=True)
