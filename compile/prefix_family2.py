"""prefix_family2.py : transcripts 0 2 4 6 8 + five more digits, where the five are three odd digits and two even digits,
   repeats allowed, in any order.  For each: number of ways to choose write and move for the wires seen (mirror removed).
   Thought tool only."""
import itertools
from collections import Counter
import transcript_to_tnf as X
D=X.D;odd=[1,3,5,7,9,11,13];even=[0,2,4,6,8,10,12]
def consistent(seq):
    nxt={}
    for a,b in zip(seq,seq[1:]):
        if nxt.setdefault(a,b//2)!=b//2: return False
    return True
res={}
for pos in itertools.combinations(range(5),3):
    for o in itertools.product(odd,repeat=3):
        for e in itertools.product(even,repeat=2):
            t=[None]*5;oi=iter(o);ei=iter(e)
            for i in range(5): t[i]=next(oi) if i in pos else next(ei)
            seq=[0,2,4,6,8]+t
            res[tuple(t)]=len(X.solve(seq))//2 if consistent(seq) else -1
c=Counter(res.values())
print("strings:",len(res),"| not a transcript:",c[-1],"| transcript but no table:",c[0],"| at least one table:",sum(v for k,v in c.items() if k>0))
hit=sorted(t for t,v in res.items() if v==258)
print("strings with exactly 258 ways:",len(hit))
fam=Counter(" ".join(D[x] for x in t[:3]) for t in hit)
for k,v in fam.items(): print("   0 2 4 6 8",k,"+ 2 more :",v,"strings")
def canon(t):
    new=[q for q in dict.fromkeys(x//2 for x in t) if q>=5]
    return new in ([],[5],[5,6])
print("with F named before G:",sum(1 for t in hit if canon(t)))
print("most common counts:"," ".join("%d:%d"%(k,v) for k,v in sorted(((k,v) for k,v in c.items() if k>0),key=lambda x:-x[1])[:8]))
