"""gate_test.py TABLE... | --list FILE : does a machine have a gate that can fire?  A test that needs no reading of its code.
   1. Run the table from a blank tape and keep some visits (head on a fresh cell at the right or left end), each as a list of
      words (a run of 1s with the 0s after it) with their repeat counts.
   2. Make many small tapes of the same form: same words in the same order, but every repeat count and every long run of 1s shrunk to
      a small random number.  Start the machine on each from the same state and end, and see whether it HALTS within a short run.
   A machine whose halt can be met halts on a fair share of these (Jeff Ketchersid's and Pavel Kropitz's champions do).
   A machine with no reachable halt halts on none (the row-of-41 holdout).  This is a test, not a proof either way."""
import sys,random
def parse(t):
    T={}
    for q,row in enumerate(t.split('_')):
        for b in (0,1):
            e=row[b*3:b*3+3];T[(q,b)]=None if e[2] in 'Z-' else (int(e[0]),1 if e[1]=='R' else -1,ord(e[2])-65)
    return T
def runs_of(tape,lo,hi):
    ws=[];i=lo
    while i<=hi and not tape.get(i,0): i+=1
    while i<=hi:
        a=0
        while tape.get(i,0): a+=1;i+=1
        b=0
        while i<=hi and not tape.get(i,0): b+=1;i+=1
        ws.append((a,b))
    out=[]
    for w in ws:
        if out and out[-1][0]==w: out[-1][1]+=1
        else: out.append([w,1])
    return out
def visits(T,n,keep=60):
    tape={};pos=0;st=0;lo=hi=0;out=[]
    for step in range(n):
        v=tape.get(pos,0)
        if v==0 and step>50 and (pos==hi or pos==lo):
            out.append((step,st,"R" if pos==hi else "L",runs_of(tape,lo,hi)))
        e=T[(st,v)]
        if e is None: return out,True
        tape[pos]=e[0];pos+=e[1];st=e[2]
        if pos<lo: lo=pos
        if pos>hi: hi=pos
    return out,False
def build(runs,side):
    cells=[]
    for (a,b),k in runs: cells+=([1]*a+[0]*b)*k
    if side=="R":
        if not cells or cells[-1]==1: cells.append(0)
        return {i:1 for i,v in enumerate(cells) if v},len(cells)-1
    return {i:1 for i,v in enumerate(cells) if v},-1
def halts(T,tape,pos,st,n):
    for step in range(n):
        e=T[(st,tape.get(pos,0))]
        if e is None: return True
        tape[pos]=e[0];pos+=e[1];st=e[2]
    return False
def test(tm,steps=3000000,trials=600,short=150000,seed=1):
    T=parse(tm);rnd=random.Random(seed)
    v,h=visits(T,steps)
    if h: return "halts by itself within %d steps"%steps
    if len(v)<10: return "too few visits (%d)"%len(v)
    pick=[v[i] for i in sorted(set(int(len(v)*f) for f in (0.3,0.4,0.5,0.6,0.7,0.8,0.9,0.95,0.99)))]
    nh=0;ex=None
    for t in range(trials):
        step,st,side,runs=pick[t%len(pick)]
        new=[]
        for (a,b),k in runs:
            a2=a if a<=8 else rnd.randint(1,8)
            k2=k if k==1 else rnd.randint(1,min(k,7))
            new.append([(a2,b),k2])
        tape,pos=build(new,side)
        if halts(T,dict(tape),pos,st,short):
            nh+=1
            if ex is None: ex=" ".join(("%d.%d"%w if k==1 else "(%d.%d)x%d"%(w[0],w[1],k)) for w,k in new)[:70]
    return "%d of %d small tapes halt%s"%(nh,trials,("; e.g. "+ex) if ex else "")
if __name__=="__main__":
    a=sys.argv[1:]
    tabs=[l.split()[0] for l in open(a[1]) if l.strip()] if a and a[0]=="--list" else a
    for t in tabs: print(t,"|",test(t.replace("1RZ","---")),flush=True)
