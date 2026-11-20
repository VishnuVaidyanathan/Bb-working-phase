"""gatescan.py [KMAX [MMAX]] : every gate choice followed from a blank tape by arithmetic (stackcalc.py + remainder.py).
   K = cells a round adds, m = size of a fresh store, RH = leftover that halts.
   Small rows are run plainly.  The first row too big for that is ended by formula (exact remainder).
   If it survives, the next row has a tower-sized number of stores n.  The leftover at the end of a fresh row of n stores
   is computed for n = 1..16 and repeats with a short period (observed, not proved); the remainder of n by that period
   then decides the tower-sized row:  HALT there (size: tower-many arrows), or survive again (then unknown), or
   the leftover can never be RH again (never halts)."""
import sys,time
import stackcalc as S,remainder as R
_ends={}
def ends(K,m,last,nmax=16):
    key=(K,m,last)
    if key not in _ends:
        D=S.Design(K,m);out=[]
        for n in range(1,nmax+1):
            stores=[m]*(n-(1 if last else 0))+([last] if last else [])
            out.append((R.mod_(D.row_end(m,stores),m,{})+K)%m)
        _ends[key]=out
    return _ends[key]
def pattern(seq):
    """(start, period) of the repeating tail of seq (1-based n), or None"""
    for p in (1,2,3,4):
        for s in range(0,7):
            tail=seq[s:]
            if len(tail)>=3*p and all(tail[i]==tail[i%p] for i in range(len(tail))): return s,p
    return None
def verdict(K,m,RH):
    D=S.Design(K,m);rows=[];w=0;stores=[]
    for _ in range(40):
        res=S.plain(K,m,RH,w,stores,bits=20000,maxev=200000) if len(stores)<=60 else ("BIG",None)
        if res[0]=="HALT": return "halts small (inside a row)",rows
        if res[0]=="ROW":
            marks=S.cut(res[1]+K,m,RH)
            if marks is None: return "halts small (end of a small row)",rows
            rows.append(len(marks)-1);w=marks[0];stores=marks[1:];continue
        break
    else: return "still small after 40 rows",rows
    n1=len(stores);Wf=D.row_end(w,stores)
    r=(R.mod_(Wf,m,{})+K)%m
    if r==RH: return "HALTS at the end of the row of %d stores: about %d arrows"%(n1,max(0,n1-2)),rows
    # next row: n stores, tower-sized.  n = k-1+[r>0],  k=(W+K-r)/m
    seq=ends(K,m,r);pat=pattern(seq)
    if pat is None: return "survives the row of %d; next row tower-sized; no simple pattern %s"%(n1,seq),rows
    s,p=pat;cyc=seq[s:s+p]
    if RH not in cyc: return "NEVER HALTS after the row of %d (leftovers of long rows are %s, never %d)"%(n1,sorted(set(cyc)),RH),rows
    k=((R.mod_(Wf,m*p,{})+K-r)%(m*p))//m
    n=(k-1+(1 if r else 0))%p
    left=cyc[(n-1-s)%p]                    # seq index is n-1
    if left==RH: return "HALTS at the end of the 2nd big row: tower-many arrows (rows: %d stores, then a tower-sized number)"%n1,rows
    return "survives the row of %d AND the tower-sized row (leftover %d); after that unknown"%(n1,left),rows
if __name__=="__main__":
    KM=int(sys.argv[1]) if len(sys.argv)>1 else 11;MM=int(sys.argv[2]) if len(sys.argv)>2 else 7
    for m in range(2,MM+1):
        for K in range(1,KM+1):
            for RH in range(1,m):
                t=time.time()
                try: v,rows=verdict(K,m,RH)
                except Exception as e: v,rows="ERROR "+str(e)[:60],[]
                print("store %d, round +%2d, halt on %d left | rows %-28s | %s"%(m,K,RH,rows,v),flush=True)
