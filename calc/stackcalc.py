"""stackcalc.py : the stack design followed by arithmetic all the way to the end of a row, with exact remainders.

   Design numbers:  K = cells one round adds,  m = size of a fresh store,  RH = the leftover that halts.
   A row is a block b and stores s1..sn.  Working through a row (proved by induction from the event rules, tested against
   the plain event-by-event run wherever that run can be finished):
        level 0 rule   P0(x) = x + K
        level g rule   Pg(x) = P(g-1) repeated (x + K - m*g) times, starting from c(g-1)      (one payment at level g+1)
        c(0) = m,   c(j) = P(j-1) repeated m times from c(j-1)                               (a fresh row of j stores used up)
        block at the end of the row = P(n-1)^(sn) ( ... P1^(s2) ( P0^(s1) (b) ) ... )
   End of a row: W + K cells are cut into stores of m; leftover RH halts; otherwise the stores are the next row.
   Sizes: a row of n stores ends with a number of about n-2 arrows.
   Usage: python3 stackcalc.py --test | --scan | K m RH [FIRSTBLOCK]"""
import sys
import remainder as R
sys.setrecursionlimit(1000000)

class N(tuple):                      # a formula node; equal only to itself, so shared parts are computed once
    __hash__=lambda s: id(s)
    __eq__=lambda s,o: s is o
    __ne__=lambda s,o: s is not o
_pool={}
def node(*parts):
    key=tuple(id(p) if isinstance(p,N) else p for p in parts)
    if key not in _pool:
        n=N(parts);n.closed=all(getattr(p,"closed",True) for p in parts if isinstance(p,N)) and parts[0]!="var"
        if parts[0]=="iter": n.closed=parts[3].closed and parts[4].closed      # the rule's own variable is bound
        _pool[key]=n
    return _pool[key]
def num(v): return node("num",v)
def add(a,b): return node("add",a,b)
def var(name): return node("var",name)

# caches for closed formulas (the calculator itself is unchanged)
_modc={};_exc={}
_mod0=R.mod_;_ex0=R.exact
def mod_cached(e,m,env):
    if isinstance(e,N) and e.closed:
        k=(id(e),m)
        if k not in _modc: _modc[k]=_mod0(e,m,env)
        return _modc[k]
    return _mod0(e,m,env)
def exact_cached(e,env):
    if isinstance(e,N) and e.closed:
        k=id(e)
        if k not in _exc: _exc[k]=_ex0(e,env)
        return _exc[k]
    return _ex0(e,env)
R.mod_=mod_cached;R.exact=exact_cached

class Design:
    def __init__(s,K,m): s.K=K;s.m=m;s._c={}
    def P(s,g,X):
        """level g rule applied to formula X"""
        if g==0: return add(X,num(s.K))
        v=var("v%d"%g)
        return node("iter",s.P(g-1,v),"v%d"%g,s.c(g-1),add(X,num(s.K-s.m*g)))
    def c(s,j):
        if j not in s._c:
            if j==0: s._c[j]=num(s.m)
            else:
                v=var("u%d"%j);s._c[j]=node("iter",s.P(j-1,v),"u%d"%j,s.c(j-1),num(s.m))
        return s._c[j]
    def row_end(s,b,stores):
        """formula for the block when the row (block b, exact stores list) is used up"""
        X=b if isinstance(b,N) else num(b)
        for j,sj in enumerate(stores,1):
            v=var("w%d"%j);X=node("iter",s.P(j-1,v),"w%d"%j,X,sj if isinstance(sj,N) else num(sj))
        return X

# ---------- plain event-by-event run (exact, only while numbers are small) ----------
def plain(K,m,RH,w,stores,bits=200000,maxev=2000000):
    """returns ('HALT',w,None) | ('ROW',w_at_row_end,None) at the first time nothing is behind | ('BIG',..)"""
    stores=list(stores);ev=0
    while ev<maxev:
        ev+=1
        while stores and stores[-1]==0: stores.pop()
        if not stores: return ("ROW",w)
        if stores[0]>0:
            w+=K*stores[0];stores[0]=0
            if w.bit_length()>bits: return ("BIG",None)
            continue
        g=0
        while stores[g]==0: g+=1
        d=stores[g];rest=stores[g+1:];avail=w+K
        if avail>m*g: w=m;stores=[m]*(g-1)+[avail-m*g,d-1]+rest
        else:
            k,r=divmod(avail,m)
            if r==RH: return ("HALT",w)
            marks=[m]*k+([r] if r else [])
            w=marks[0];stores=marks[1:]+[0]*max(0,g-len(marks))+[d]+rest
    return ("BIG",None)

def cut(avail,m,RH):
    k,r=divmod(avail,m)
    if r==RH: return None
    return [m]*k+([r] if r else [])

def arrows(n): return max(0,n-2)
def fate(K,m,RH,first=0,maxrows=12,say=None):
    """follow the design from a first block (0 = blank tape).  Returns (verdict, list of row lengths, note)."""
    D=Design(K,m);rows=[];w=first;stores=[]
    for _ in range(maxrows):
        # the row (w, stores) : try the plain run, else the formula
        res=plain(K,m,RH,w,stores,bits=20000,maxev=200000) if len(stores)<=40 else ("BIG",None)
        if res[0]=="HALT": return ("HALT inside a small row",rows,"last block %d"%res[1])
        if res[0]=="ROW":
            W=res[1];marks=cut(W+K,m,RH)
            if marks is None: return ("HALT at the end of row %d"%len(rows),rows,"about %d arrows"%arrows(rows[-1]) if rows else "small")
            rows.append(len(marks)-1);w=marks[0];stores=marks[1:];continue
        # numbers too big: formula for the end of this row, then its remainder
        Wf=D.row_end(w,stores)
        r=(R.mod_(Wf,m,{})+K)%m
        if r==RH: return ("HALT at the end of row %d"%len(rows),rows,"about %d arrows"%arrows(rows[-1]))
        return ("SURVIVES row %d : the next row is tower-sized"%len(rows),rows,"leftover %d; next row has more stores than can be written"%r)
    return ("still small after %d rows"%maxrows,rows,"")

def selftest():
    bad=0;n=0
    for K in (1,2,3,4,5,7):
        for m in (2,3,4,5):
            D=Design(K,m)
            for b in (m,m+1,7):
                for stores in ([m],[m,m],[m,m,m],[m,1],[m,m,2],[3,2,2],[m,m,m,1],[2,2,2,2],[m,m,m,m]):
                    res=plain(K,m,None,b,stores,bits=3000000,maxev=3000000)
                    if res[0]!="ROW": continue
                    W=res[1];f=D.row_end(b,stores)
                    for M in (2,3,4,5,6,7,8,9,12,m,2*m,m*m):
                        _modc.clear();got=R.mod_(f,M,{});n+=1
                        if got!=W%M: bad+=1;print("WRONG",K,m,b,stores,M,got,W%M)
    print("stack arithmetic self test: %d remainders of row ends compared with the plain run, %d wrong"%(n,bad))
    return bad==0
if __name__=="__main__":
    a=sys.argv[1:]
    if a and a[0]=="--test": sys.exit(0 if selftest() else 1)
    if a and a[0]=="--scan":
        from math import gcd
        for K in range(1,10):
            for m in range(2,8):
                for RH in range(1,m):
                    v,rows,note=fate(K,m,RH)
                    print("round +%d, store %d, halt on %d left: %-45s rows %s  %s"%(K,m,RH,v,rows,note));sys.stdout.flush()
        sys.exit(0)
    K,m,RH=int(a[0]),int(a[1]),int(a[2]);first=int(a[3]) if len(a)>3 else 0
    print(fate(K,m,RH,first))
