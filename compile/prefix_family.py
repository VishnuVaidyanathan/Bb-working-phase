"""prefix_family.py : Vishnu's question of 24 Nov.  Transcripts 0 2 4 6 8 + five more digits, where the five are
   four odd digits made of three different ones (one of them twice) and one even digit, in any order (Jeff Ketchersid's
   start  0 2 4 6 8 b b a 1 d  is one of them).  For each, how many ways are there to choose write and move for the wires
   seen (mirror image removed)?  A string where the same wire is followed by two different states is not a transcript at all.
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
tails=set()
for trio in itertools.combinations(odd,3):
    for rep in trio:
        four=list(trio)+[rep]
        for e in even:
            for p in set(itertools.permutations(four+[e])): tails.add(p)
res={}
for t in sorted(tails):
    seq=[0,2,4,6,8]+list(t)
    res[t]=len(X.solve(seq))//2 if consistent(seq) else -1
c=Counter(res.values())
print("strings:",len(res))
print("not a transcript (one wire followed by two different states):",c[-1])
print("a transcript, but no table gives it:",c[0])
print("at least one table:",sum(v for k,v in c.items() if k>0))
print("number of ways -> how many strings:"," ".join("%d:%d"%(k,c[k]) for k in sorted(c) if k>0))
hit=[t for t,v in res.items() if v==258]
print("strings with exactly 258 ways:",len(hit))
for t in hit: print("   0 2 4 6 8 "+" ".join(D[x] for x in t))
canon=[t for t,v in res.items() if v>0 and (lambda s:[q for q in dict.fromkeys(x//2 for x in s) if q>=5] in ([],[5],[5,6]))(t)]
print("of those with a table, F is named before G (no double counting by names):",len(canon))
cc=Counter(res[t] for t in canon);print("   ways -> strings:"," ".join("%d:%d"%(k,cc[k]) for k in sorted(cc)))
print("   with exactly 258 ways:",sum(1 for t in canon if res[t]==258))
