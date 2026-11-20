"""model.py : Jeff Ketchersid's champion as arithmetic on (block; stores), checked against his real run at every home visit.
   Rules (read from thought experiments, rules.py):
     round            : front store > 0                 ->  block +3, front store -1
     ticket           : g empty levels, payer d >= 2    ->  block 1, g-1 stores of 2, then (block + 7 - 2g), payer d-2
     payer of 1 with a real store behind it             ->  HALT
     end of the row (payer 1, nothing real behind)      ->  block odd: HALT;  block even: a new row (see new_row)"""
import sys,homes as H
def new_row(w,g,rest):
    # read from experiments for rest = [] , [1] , [0,1] ; anything else is not modelled
    n=w//2
    if rest==[]: extra=0
    elif rest==[1]: extra=1
    elif rest==[0,1]: extra=None
    else: return None
    if g==1:
        if extra is None: return (3,[3]+[2]*(n+1)+[1])
        return (3+extra,[2]*(n+1+extra)+[1])
    if extra is None: return (2,[2]*(g-2)+[3,3]+[2]*(n-(g-2))+[1])
    return (2,[2]*(g-2)+[3+extra]+[2]*(n-(g-2)+extra)+[1])
def step(w,st):
    st=list(st)
    if st and st[0]>0: st[0]-=1;return (w+3,st)
    g=0
    while g<len(st) and st[g]==0: g+=1
    if g==len(st): return None
    d=st[g];rest=st[g+1:]
    if d>=2: return (1,[2]*(g-1)+[w+7-2*g,d-2]+rest)
    if any(x>=2 for x in rest): return "HALT"
    if w%2: return "HALT"
    return new_row(w,g,rest)
def dec(r):
    w=r[0][0] if r else 0;st=[]
    for i,(a,b) in enumerate(r):
        if i>0: st.append(a)
        if i<len(r)-1: st+=[0]*((b-2)//2)
    return w,st
if __name__=="__main__":
    n=int(sys.argv[1]) if len(sys.argv)>1 else 30000000
    h,halt=H.homes(H.J,n)
    cfg=[dec(r) for s,l,r in h if l==1]
    ok=bad=0;first=None
    for a,b in zip(cfg[2:],cfg[3:]):
        m=step(*a)
        if m is not None and m!="HALT" and (m[0],list(m[1]))==(b[0],list(b[1])): ok+=1
        else:
            bad+=1
            if first is None: first=(a,m,b)
    print("home visits compared: %d agree, %d differ"%(ok,bad))
    if first: print("first difference:",str(first)[:400])
