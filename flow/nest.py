"""nest.py TABLE [STEPS] : the nest of the filler.
   Take the most used loop (a digit that repeats, or two digits that alternate) and list the length of every run of it, in order.
   Depth 1, a plain grid: the lengths only climb (4, 9, 14, ...).
   Depth 2: they climb and fall back (a saw), and the tops of the teeth only climb.
   Depth 3: the tops themselves climb and fall back.  And so on."""
import sys,re
from collections import Counter
H="0123456789abcd"
def transcript(tm,NS):
    T={}
    for s,x in enumerate(tm.split("_")):
        for k in (0,1):
            e=x[3*k:3*k+3];T[(s,k)]=None if e[2] in "Z-" else (int(e[0]),1 if e[1]=="R" else -1,ord(e[2])-65)
    N=300000;tape=bytearray(2*N);p=N;s=0;d=bytearray()
    for i in range(NS):
        r=tape[p];d.append(ord(H[2*s+r]));t=T[(s,r)]
        if t is None: break
        tape[p]=t[0];p+=t[1];s=t[2]
        if p<5 or p>2*N-5: break
    return d.decode()
def runs(S):
    c=Counter(zip(S,S[1:]))
    best=None
    for (a,b),n in c.items():
        if a==b: sc=n;pat="(?:%s)+"%a;w=1
        elif c.get((b,a),0)>0.8*n: sc=n+c[(b,a)];pat="(?:%s%s)+"%(a,b);w=2
        else: continue
        if best is None or sc>best[0]: best=(sc,pat,w,a+b if w==2 else a)
    if not best: return None,[]
    return best[3],[len(m.group(0))//best[2] for m in re.finditer(best[1],S)]
def tops(seq):
    """the top of every tooth.  A tooth is a climb and then a fall: the top is recorded once the lengths have fallen to
       70 percent of it or less, and the next tooth starts only when they have climbed again by the same margin."""
    out=[];m=None;lo=None;rising=True
    for x in seq:
        if rising:
            if m is None or x>m: m=x
            elif x<=0.7*m: out.append(m);rising=False;lo=x
        else:
            if x<lo: lo=x
            elif x*0.7>=lo: rising=True;m=x
    return out
def depth(seq):
    d=1;trail=[]
    while True:
        t=tops(seq)
        if len(t)<2: break
        d+=1;trail.append(t);seq=t
        if d>20: break
    return d,trail
if __name__=="__main__":
    tm=sys.argv[1];NS=int(sys.argv[2]) if len(sys.argv)>2 else 2000000
    S=transcript(tm,NS);loop,r=runs(S);r=[x for x in r if x>=2]
    d,trail=depth(r)
    print("filler",loop," runs",len(r)," nest depth",d)
    print("  run lengths:",r[:40])
    for i,t in enumerate(trail): print("  tops, level %d:"%(i+1),t[:14],"..." if len(t)>14 else "")
