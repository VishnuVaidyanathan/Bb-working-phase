"""doors.py TABLE [STEPS] : find the round of a machine and list its doors.
   Real run from a blank tape.  The run is cut each time one chosen wire fires; the round is the set of wires of the most repeated
   cut that moves both left and right.  A door = the unused half of a state the round uses.  A free state = a state the round
   never enters.  Prints the round, the doors, the free states, where the halt sits, and how often each non-round wire fired.
   Thought tool only."""
import sys
from collections import Counter
def parse(t):
    T={}
    for q,r in enumerate(t.split("_")):
        for b in (0,1):
            e=r[b*3:b*3+3];T[(q,b)]=e if e[2] in "-Z" else (int(e[0]),1 if e[1]=="R" else -1,ord(e[2])-65)
    return T
def study(t,n=2000000):
    T=parse(t);tape={};pos=0;st=0;seq=[];halt=None
    for k in range(n):
        v=tape.get(pos,0);e=T[(st,v)]
        if isinstance(e,str): halt=k;break
        seq.append(st*2+v);tape[pos]=e[0];pos+=e[1];st=e[2]
    S=len(t.split("_"));best=None
    for x in range(2*S):
        c=Counter();cur=set()
        for w in seq:
            if w==x:
                if cur: c[frozenset(cur)]+=1
                cur=set()
            cur.add(w)
        for sig,m in c.most_common(3):
            dirs={T[(w//2,w%2)][1] for w in sig}
            if len(dirs)==2 and (best is None or m>best[0]): best=(m,sig,x)
    name=lambda w:"ABCDEFGHIJ"[w//2]+str(w%2)
    m,sig,x=best;used=Counter(seq);rs={w//2 for w in sig}
    doors=[w for w in range(2*S) if w//2 in rs and w not in sig]
    free=[q for q in range(S) if q not in rs]
    print(t);print("  steps run:",len(seq),"(halted)" if halt is not None else "")
    print("  round: %d wires in %d states, seen %d times:"%(len(sig),len(rs),m)," ".join(name(w) for w in sorted(sig)))
    print("  doors (free half of a round state):"," ".join(name(w)+"="+(T[(w//2,w%2)] if isinstance(T[(w//2,w%2)],str) else t.split("_")[w//2][(w%2)*3:(w%2)*3+3])+"(%d)"%used[w] for w in doors) or "none")
    print("  free states:"," ".join("ABCDEFGHIJ"[q]+"(%d,%d)"%(used[2*q],used[2*q+1]) for q in free) or "none")
    return len(sig),len(rs),len(doors),len(free)
if __name__=="__main__":
    study(sys.argv[1],int(sys.argv[2]) if len(sys.argv)>2 else 2000000)
