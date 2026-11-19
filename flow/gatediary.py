"""gatediary.py TABLE [STEPS] : the diary of the gate.
   Finds the counting loop the halt hangs off (2 or 3 digits repeating, like 159), then lists every visit to it in order:
   how many times round, and which way the run left (the next two digits).  The halt is one of the ways out."""
import sys,re
from collections import Counter
sys.path.insert(0,__file__.rsplit("/",1)[0])
from nest import transcript
H="0123456789abcd"
def diary(tm,NS):
    S=transcript(tm,NS);ent={}
    for s,x in enumerate(tm.split("_")):
        for k in (0,1): ent[2*s+k]=x[3*k:3*k+3]
    hd=[d for d,e in ent.items() if e[2]=="Z"]
    if not hd: return None
    hd=hd[0];nx={d:(None if e[2] in "Z-" else ord(e[2])-65) for d,e in ent.items()}
    def dist(cyc):
        best=9
        for c in cyc:
            cur=[H.index(c)^1]
            for dd in (1,2,3):
                nf=[]
                for y in cur:
                    if y==hd: best=min(best,dd)
                    elif nx[y] is not None: nf+= [2*nx[y],2*nx[y]+1]
                cur=nf
        return best
    cands=Counter()
    for K in (3,2):
        for m in re.finditer(r'(?=((.{%d})\2{2,}))'%K,S):
            w=m.group(2)
            if len(set(w))>1: cands[min(w[i:]+w[:i] for i in range(K))]+=1
    best=None
    for w,n in cands.items():
        d=dist(w)
        if d<9 and (best is None or (d,-n)<(best[0],-best[1])): best=(d,n,w)
    if not best: return None
    d,n,w=best;K=len(w);rots=[w[i:]+w[:i] for i in range(K)];out=[]
    pat=re.compile("(?:"+"|".join("(?:%s)+"%r for r in rots)+")")
    for m in re.finditer(pat,S):
        r=len(m.group(0))//K
        if r>=1: out.append((m.start()+1,r,S[m.end():m.end()+2]))
    return w,d,H[hd],out
if __name__=="__main__":
    tm=sys.argv[1];NS=int(sys.argv[2]) if len(sys.argv)>2 else 2000000
    r=diary(tm,NS)
    if not r: print("no counting loop near the halt");sys.exit()
    w,d,hd,out=r;big=[o for o in out if o[1]>=2]
    print("counting loop %s, halt digit %s is %d step(s) from it, %d visits of 2 or more rounds"%(w,hd,d,len(big)))
    print("ways out so far:",dict(Counter(o[2] for o in big)))
    for st,rr,ex in big[:int(sys.argv[3]) if len(sys.argv)>3 else 30]: print("  step %10d  rounds %7d  remainder by %d: %d  leaves by %s"%(st,rr,len(w),rr%len(w),ex))
