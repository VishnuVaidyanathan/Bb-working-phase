"""model.py : Pavel Kropitz's machine as arithmetic on a list of counters, checked against his real run.
   Canonical visit: lead word, counters, the last counter b at the right end.
     transfer : the counter a next to the last one is not empty   ->  a-1, b+2
     ticket   : g empty counters before the last one, payer c >= 3 before them
                ->  payer c-3 ; then b+7 (g = 1)  or  b+5, g-2 counters of 3, a counter of 5 (g >= 2) ; then a new last counter 0
     payer of 1, or a payer of 2 with something to its left      ->  HALT   (thought experiments, rules.py)
     payer of 2 at the left end                                  ->  the lead word grows (row event; not modelled here)"""
import sys,counters as C,rules as R
def step(lead,cs):
    cs=list(cs)
    if len(cs)>=2 and cs[-2]>0: cs[-2]-=1;cs[-1]+=2;return lead,cs
    b=cs[-1];g=0;i=len(cs)-2
    while i>=0 and cs[i]==0: g+=1;i-=1
    if i<0: return None
    c=cs[i]
    if c>=3:
        new=[b+7] if g==1 else [b+5]+[3]*(g-2)+[5]
        return lead,cs[:i]+[c-3]+new+[0]
    if c==1 or i>0: return "HALT"
    return None
if __name__=="__main__":
    n=int(sys.argv[1]) if len(sys.argv)>1 else 30000000
    v=[R.canon(c) for s,c in C.visits(n) if c!="HALT"]
    v=[x for x in v if x is not None]
    ok=bad=skip=0;first=None
    for a,b in zip(v,v[1:]):
        m=step(*a)
        if m is None: skip+=1
        elif m!="HALT" and (m[0],list(m[1]))==(b[0],list(b[1])): ok+=1
        else:
            bad+=1
            if first is None: first=(a,m,b)
    print("canonical visits compared: %d agree, %d differ, %d are cases not modelled (left end / row events)"%(ok,bad,skip))
    if first: print("first difference:",str(first)[:500])
