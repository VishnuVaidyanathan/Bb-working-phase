"""transcript_pavel.py [CUT] [LINES] [SKIP] : Pavel Kropitz's BB7 machine written as a transcript in Vishnu's digits
   (A0=0 A1=1 B0=2 B1=3 C0=4 C1=5 D0=6 D1=7 E0=8 E1=9 F0=a F1=b G0=c G1=d), repeats folded as 1x7.
   Real run from a blank tape, cut into lines each time digit CUT fires (default 0), with the tape as run lengths.
   Thought tool; credit for the machine: Pavel Kropitz."""
import sys
from collections import Counter
t="1RB0RA_1LC1LF_1RD0LB_1RA1LE_1RZ0LC_1RG1LD_0RG0RF";D="0123456789abcd"
cut=sys.argv[1] if len(sys.argv)>1 else "0";lines=int(sys.argv[2]) if len(sys.argv)>2 else 30;skip=int(sys.argv[3]) if len(sys.argv)>3 else 0
rows=t.split("_");T={}
for q,r in enumerate(rows):
    for b in (0,1):
        e=r[b*3:b*3+3];T[(q,b)]=None if e[2]=="Z" else (int(e[0]),1 if e[1]=="R" else -1,ord(e[2])-65)
def fold(s):
    o=[]
    for d in s:
        if o and o[-1][0]==d: o[-1][1]+=1
        else: o.append([d,1])
    # fold repeated pairs/words is left to the eye
    return " ".join(d if k==1 else "%sx%d"%(d,k) for d,k in o)
def shape():
    ks=[k for k,v in tape.items() if v]
    if not ks: return "(blank)"
    lo,hi=min(ks),max(ks);out=[];q=lo
    while q<=hi:
        a=0
        while tape.get(q,0): a+=1;q+=1
        z=0
        while q<=hi and not tape.get(q,0): z+=1;q+=1
        out.append(str(a)+"_"*(z-1))
    return " ".join(out)
tape={};pos=0;st=0;seq=[];n=0;use=Counter()
for k in range(3000000):
    v=tape.get(pos,0);d=D[st*2+v]
    if d==cut and seq:
        n+=1
        if skip<n<=skip+lines: print("%7d  %s   -> %s"%(k,fold(seq)[:150],shape()[:70]))
        seq=[]
    e=T[(st,v)]
    if e is None: break
    seq.append(d);use[d]+=1;tape[pos]=e[0];pos+=e[1];st=e[2]
print("how often each digit fired in 3,000,000 steps:"," ".join("%s:%d"%(d,use[d]) for d in D))
