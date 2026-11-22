"""transfer.py FILE [STEPS] : for each table, the commonest "transfer" seen between two visits of the far end in the same state:
   which two numbers on the tape changed, and by how much (payer -p, gainer +q).  Numbers are either repeat counts of a word
   (word layout) or lengths of solid runs (counter layout).  A thought tool: it only reports what is commonest in the first STEPS steps."""
import sys
from collections import Counter
exec(open(__import__("os").path.join(__import__("os").path.dirname(__import__("os").path.abspath(__file__)),"view.py")).read().split("t=sys.argv[1]")[0])
def groups(w):
    g=[];i=0
    while i<len(w):
        j=i
        while j<len(w) and w[j]==w[i]: j+=1
        g.append((w[i],j-i));i=j
    return g
def study(t,n):
    T=parse(t);out={}
    for side in "RL":
        tape={};pos=0;st=0;lo=hi=0;prev={};cw=Counter();cr=Counter()
        for s in range(n):
            v=tape.get(pos,0)
            if v==0 and ((side=="R" and pos==hi) or (side=="L" and pos==lo)):
                w=words(tape,lo,hi)
                if w and w[-1][1]: w[-1]=(w[-1][0],0)
                g=groups(w);key=st
                if key in prev:
                    pg,pw=prev[key]
                    if [x[0] for x in pg]==[x[0] for x in g]:
                        d=[(i,b[1]-a[1]) for i,(a,b) in enumerate(zip(pg,g)) if a[1]!=b[1]]
                        if len(d)==2 and d[0][1]*d[1][1]<0: cw[tuple(sorted((d[0][1],d[1][1])))+(g[d[0][0]][0],g[d[1][0]][0])]+=1
                    if len(pw)==len(w) and [x[1] for x in pw]==[x[1] for x in w]:
                        d=[b[0]-a[0] for a,b in zip(pw,w) if a[0]!=b[0]]
                        if len(d)==2 and d[0]*d[1]<0: cr[tuple(sorted(d))]+=1
                prev[key]=(g,w)
            e=T[(st,v)]
            if e is None: break
            tape[pos]=e[0];pos+=e[1];st=e[2];lo=min(lo,pos);hi=max(hi,pos)
        out[side]=(cw.most_common(2),cr.most_common(2))
    return out
if __name__=="__main__":
    n=int(sys.argv[2]) if len(sys.argv)>2 else 300000
    for l in open(sys.argv[1]):
        p=l.split()
        if not p: continue
        r=study(p[0],n);best=[]
        for side in "RL":
            for (k,c) in r[side][0]: best.append((c,"words: pay %d, gain %d (%s -> %s)"%(-k[0],k[1],"%d.%d"%k[2],"%d.%d"%k[3])))
            for (k,c) in r[side][1]: best.append((c,"solid runs: pay %d, gain %d"%(-k[0],k[1])))
        best.sort(reverse=True)
        print(p[0],"|"," ".join(p[1:])[:18],"|"," ; ".join("%s x%d"%(b,a) for a,b in best[:3]) or "no transfer seen",flush=True)
