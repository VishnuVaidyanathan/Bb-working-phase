"""combos.py : Vishnu's question (24 Nov): the transcript starts 0 2 4 6 8 and five more digits follow,
   four odd digits and one even digit, in any order.  For every such string: how many tables produce it
   (ways to choose write and move for the wires seen, mirror image removed)?  Counted twice: the four odd digits all
   different, and repeats allowed (Jeff Ketchersid's own start, b b a 1 d, has a repeat).  Thought tool only."""
import itertools
from collections import Counter
import transcript_to_tnf as X
D=X.D;odd=[1,3,5,7,9,11,13];even=[0,2,4,6,8,10,12];base=[0,2,4,6,8]
def run(distinct):
    res={}
    for p in range(5):
        for e in even:
            it=itertools.permutations(odd,4) if distinct else itertools.product(odd,repeat=4)
            for o in it:
                tail=list(o);tail.insert(p,e)
                n=len(X.solve(base+tail))//2
                res[" ".join(D[x] for x in tail)]=n
    return res
for distinct in (True,False):
    r=run(distinct);c=Counter(r.values());live={k:v for k,v in r.items() if v}
    print("four odd digits","all different" if distinct else "repeats allowed",": strings",len(r),"| strings some table produces:",len(live))
    print("   number of tables -> how many strings:"," ".join("%d:%d"%(k,c[k]) for k in sorted(c) if k)[:600])
    print("   strings with exactly 258:",sum(1 for v in r.values() if v==258),[k for k,v in r.items() if v==258][:12])
    top=sorted(live.items(),key=lambda x:-x[1])[:6];print("   most tables:",top)
