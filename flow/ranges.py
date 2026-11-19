"""ranges.py TABLE [STEPS] : the ranges of a machine.  Every road (digit -> next digit) is counted, and roads used about
   equally often (within 8 percent) are put in one range.  Prints each range: how often, and which roads."""
import sys
from collections import Counter
sys.path.insert(0,__file__.rsplit("/",1)[0])
from nest import transcript
def ranges(tm,NS):
    S=transcript(tm,NS);c=Counter(zip(S,S[1:]));items=sorted(c.items(),key=lambda x:x[1]);out=[]
    for (a,b),n in items:
        if out and n<=out[-1][0]*1.08: out[-1][1].append(a+b);out[-1][2]=n
        else: out.append([n,[a+b],n])
    return out
if __name__=="__main__":
    tm=sys.argv[1];NS=int(sys.argv[2]) if len(sys.argv)>2 else 1000000
    for lo,roads,hi in ranges(tm,NS):
        print("  %10s%s  %2d roads: %s"%(format(lo,","),"" if hi==lo else " to "+format(hi,","),len(roads)," ".join(roads)))
