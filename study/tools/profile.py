"""One-line profile of a machine from a plain run: when all wires have appeared, the fillers, the tape picture."""
import sys,re,collections
from read import load,D,rl
def profile(tm,N=1500000):
    T=load(tm);tape={};p=0;s=0;cnt=collections.Counter();first={};big=collections.Counter();prev=None;halt=None;lastrare=None
    nst=len(tm.split('_'))
    for i in range(N):
        r=tape.get(p,0);d=D[2*s+r];t=T[(s,r)]
        if t is None: halt=i+1;break
        cnt[d]+=1;first.setdefault(d,i+1)
        if prev is not None: big[prev+d]+=1
        prev=d;tape[p]=t[0];p+=t[1];s=t[2]
    tot=sum(cnt.values())
    top=[d for d in sorted(cnt,key=lambda x:-cnt[x]) if cnt[d]>0.02*tot]
    # single fillers: digit followed by itself most of the time; pair fillers: xy and yx both dominant
    single=[d for d in top if big[d+d]>0.6*cnt[d]]
    pairs=[]
    for a in top:
        for b in top:
            if a<b and big[a+b]>0.6*cnt[a] and big[b+a]>0.6*cnt[b]: pairs.append(a+b)
    triples=[]
    rest=[d for d in top if d not in single and not any(d in x for x in pairs)]
    ks=[k for k in tape if tape[k]];lo,hi=min(ks),max(ks)
    pic=rl("".join(str(tape.get(k,0)) for k in range(lo,hi+1)))
    return dict(wires=len(cnt),allby=max(first.values()),order="".join(sorted(first,key=first.get)),single=single,pairs=pairs,other=rest,halt=halt,pic=pic[:150],width=hi-lo+1)
if __name__=="__main__":
    for line in open(sys.argv[1]):
        n,tm=line.split();pr=profile(tm)
        print("%-5s %s\n      wires %d, all seen by digit %d (order %s) | single fillers %s | pair fillers %s | other frequent %s%s\n      tape (width %d): %s"%(n,tm,pr['wires'],pr['allby'],pr['order'],",".join(pr['single']) or "-",",".join(pr['pairs']) or "-",",".join(pr['other']) or "-","" if not pr['halt'] else " | HALT %d"%pr['halt'],pr['width'],pr['pic']))
