"""For each seed machine: keep the wires in the order they first appear in its run; free the last K to appear
   (write, move, next state all free).  The opening of the transcript stays the seed's; what follows changes."""
import sys
D="0123456789abcd"; K=int(sys.argv[1]); only=sys.argv[2].split(",") if len(sys.argv)>2 else None
def order(tm,N=3000000):
    c=tm.split('_');T={}
    for s in range(len(c)):
        for r in range(2):
            x=c[s][3*r:3*r+3];T[(s,r)]=None if (x=='---' or x[2]=='Z') else (int(x[0]),1 if x[1]=='R' else -1,ord(x[2])-65)
    tape={};p=0;s=0;first=[]
    for i in range(N):
        r=tape.get(p,0)
        if (s,r) not in first: first.append((s,r))
        t=T[(s,r)]
        if t is None: break
        tape[p]=t[0];p+=t[1];s=t[2]
        if len(first)>=sum(1 for v in T.values() if v is not None): break
    return [k for k in first if T[k] is not None]
import itertools
opts=[w+m+q for w in "01" for m in "LR" for q in "ABCDEFG"]
for line in open("seeds.txt"):
    n,tm=line.split()
    if only and n not in only: continue
    c=tm.replace("1RZ","---").split('_')
    if len(c)!=7: continue
    o=order(tm); free=o[-K:]
    for vs in itertools.product(opts,repeat=K):
        t=[[x[:3],x[3:]] for x in c]
        for (s,r),v in zip(free,vs): t[s][r]=v
        new="_".join(a+b for a,b in t)
        if new!="_".join(c): print(n,new)
