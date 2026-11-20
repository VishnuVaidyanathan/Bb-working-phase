"""load.py TABLE [STEPS] : how much work does each wire (digit) carry?
   For every digit: the digits it comes after, the digits it goes to, and its jobs = the different (before, after) pairs it is seen in.
   Also the totals for the machine: roads used, jobs, and jobs per wire."""
import sys
from collections import Counter,defaultdict
sys.path.insert(0,__file__.rsplit("/",1)[0])
from nest import transcript
def load(tm,NS=3000000,start=None):
    S=transcript(tm,NS);jobs=defaultdict(Counter);bef=defaultdict(set);aft=defaultdict(set)
    for a,b,c in zip(S,S[1:],S[2:]): jobs[b][a+c]+=1;bef[b].add(a);aft[b].add(c)
    return S,jobs,bef,aft
if __name__=="__main__":
    tm=sys.argv[1];NS=int(sys.argv[2]) if len(sys.argv)>2 else 3000000
    S,jobs,bef,aft=load(tm,NS);what={}
    for s,x in enumerate(tm.split("_")):
        for k in (0,1):
            e=x[3*k:3*k+3];what["0123456789abcd"[2*s+k]]="halt" if e[2] in "Z-" else "%s %s %s"%(e[0],e[1],e[2])
    print(tm,"(%d digits read)"%len(S))
    tot=0;used=0
    for d in "0123456789abcd"[:2*len(tm.split("_"))]:
        if d not in jobs: print("  %s  %-7s never used"%(d,what[d]));continue
        j=jobs[d];tot+=len(j);used+=1
        print("  %s  %-7s after %-8s to %-6s jobs %2d : %s"%(d,what[d],"".join(sorted(bef[d])),"".join(sorted(aft[d])),len(j)," ".join("%s_%s(%d)"%(k[0],k[1],n) for k,n in j.most_common(9))))
    roads=len(set(zip(S,S[1:])))
    print("  wires used %d, roads %d, jobs %d, jobs per wire %.1f"%(used,roads,tot,tot/used))
