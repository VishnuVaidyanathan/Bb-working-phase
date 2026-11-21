"""wires.py [STEPS] : which wires of Jeff Ketchersid's champion work in which job.
   Real run from a blank tape; between two home visits the event is named by our checked rules (model.py):
   round, ticket (payment between depths, by number of empty levels g), new row.  For each event kind: how often it happened and
   how many times each wire fired in one typical event.  Thought tool; credit for the machine: Jeff Ketchersid."""
import sys,homes as H,model as M
from collections import Counter,defaultdict
T=H.parse(H.J);n=int(sys.argv[1]) if len(sys.argv)>1 else 3000000
tape={};pos=0;st="A";hi=0;lo=0;cur=Counter();prev=None;ev=defaultdict(list);order=[]
def read():
    runs=[];q=pos+1
    while q<=hi+1:
        a=0
        while tape.get(q,0): a+=1;q+=1
        b=0
        while q<=hi+1 and not tape.get(q,0): b+=1;q+=1
        runs.append((a,b))
    if runs and runs[-1][0]==0: runs.pop()
    return M.dec(runs),sum(tape.get(i,0) for i in range(lo,pos))
for s in range(n):
    v=tape.get(pos,0)
    if st=="A" and v==0:
        c,left=read()
        if left==1:
            if prev is not None:
                w,stz=prev;stz=list(stz)
                if stz and stz[0]>0: kind="round"
                else:
                    g=0
                    while g<len(stz) and stz[g]==0: g+=1
                    if g==len(stz): kind="other"
                    elif stz[g]>=2: kind="ticket g=%d"%g
                    else: kind="new row (g=%d)"%g
                ev[kind].append((dict(cur),prev,c))
                if kind not in order: order.append(kind)
            prev=c;cur=Counter()
    e=T[(st,v)]
    if e is None: print("HALT at",s);break
    cur[st+str(v)]+=1
    tape[pos]=e[0];pos+=e[1];st=e[2];hi=max(hi,pos);lo=min(lo,pos)
W=[q+b for q in "ABCDEFG" for b in "01"]
print("event".ljust(16),"times"," ".join(x.rjust(4) for x in W))
for k in order:
    L=ev[k];used=Counter()
    for d,_,_ in L:
        for x in d: used[x]+=1
    ex=L[min(2,len(L)-1)]
    print(k.ljust(16),str(len(L)).rjust(5)," ".join((str(ex[0].get(x,0)) if used[x] else ".").rjust(4) for x in W),"   e.g. %s -> %s"%(str(ex[1])[:38],str(ex[2])[:38]))
print("wire is used in:")
for x in W: print(" ",x,H.J.split("_")["ABCDEFG".index(x[0])][int(x[1])*3:int(x[1])*3+3],"|",", ".join(k for k in order if any(x in d for d,_,_ in ev[k])))
