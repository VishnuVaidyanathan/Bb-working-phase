"""learn41.py : collect every step between two D visits (real run and thought experiments) as "end of the token list before -> after",
   grouped by the kinds of tokens at the end.  Used to read M41's rewriting rules."""
import sys,itertools,read41 as R,rules41 as Q
from collections import defaultdict
def pairs(seq):
    seq=[c for s,st,c in seq if st=="D"]
    for a,b in zip(seq,seq[1:]):
        i=0
        while i<len(a) and i<len(b) and a[i]==b[i]: i+=1
        # keep one token of context to the left
        i=max(0,i-1)
        yield tuple(a[i:]),tuple(b[i:])
if __name__=="__main__":
    inst=defaultdict(list)
    seqs=[[(s,st,Q.dec(ws)) for s,st,ws in R.visits(3000000)]]
    for lead in ([2,"|"],[1],[]):
        for c in (0,1,2,3):
            for a in (0,1,3):
                for b in (2,5):
                    for mk in ("1.3",):
                        toks=lead+[mk]+([c] if c else [])+["|"]+([a] if a else [])+["|",b,"|"]
                        seqs.append(Q.run(toks,maxsteps=150000,maxv=4000))
    for seq in seqs:
        for a,b in pairs(seq):
            key=tuple("n" if isinstance(x,int) else x for x in a)
            if len(inst[key])<400: inst[key].append((a,b))
    print(len(inst),"kinds of step")
    for key,lst in sorted(inst.items(),key=lambda kv:-len(kv[1])):
        ex=[]
        seen=set()
        for a,b in lst:
            kb=tuple("n" if isinstance(x,int) else x for x in b)
            if kb in seen and len(ex)>=3: continue
            seen.add(kb);ex.append("%s -> %s"%(" ".join(map(str,a))," ".join(map(str,b))))
            if len(ex)>=4: break
        print("%4d  [%s]   e.g. %s"%(len(lst)," ".join(key)," ;; ".join(ex)))
