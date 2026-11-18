"""Pavel Kropitz's 7-state machine 1RB0RA_1LC1LF_1RD0LB_1RA1LE_1RZ0LC_1RG1LD_0RG0RF
read at its gate wire (state G reading 0, digit c).

  python3 pavel_gate.py trace STEPS FIRST LAST   every gate visit of the real run, left side as numbers
  python3 pavel_gate.py depth                    a lone group of x, no units  ->  2x+4 units
  python3 pavel_gate.py gate                     hand tapes: which counter sizes halt

Left side notation: a number m is a stripe group (10)^m,  .  is a single 1,  <j> is (110)^j.
Hand tapes are tests of the table, not machines."""
import re,sys
from read import load
tm="1RB0RA_1LC1LF_1RD0LB_1RA1LE_1RZ0LC_1RG1LD_0RG0RF"
def left(L):
    out=[];i=0
    while i<len(L):
        m=re.match(r'(?:10)+',L[i:])
        if m and len(m.group(0))>=2 and not (L[i:i+3]=="110" and False):
            # prefer (110)^j when it fits better
            m2=re.match(r'(?:110)+',L[i:])
            if m2 and len(m2.group(0))>=3 and len(m2.group(0))>=len(m.group(0)): out.append("<%d>"%(len(m2.group(0))//3)); i+=len(m2.group(0)); continue
            out.append(str(len(m.group(0))//2)); i+=len(m.group(0)); continue
        m2=re.match(r'(?:110)+',L[i:])
        if m2: out.append("<%d>"%(len(m2.group(0))//3)); i+=len(m2.group(0)); continue
        out.append("." if L[i]=="1" else "0"); i+=1
    s=" ".join(out)
    s=re.sub(r'(?:4 \. ){3,}',lambda m:"[4 x%d] "%(m.group(0).count("4")),s)
    return s
def right(R):
    m=re.fullmatch(r'101((?:100)*)101',R)
    if m: return "units %d"%(len(m.group(1))//3)
    m=re.fullmatch(r'10((?:110)*)1',R)
    if m: return "units' %d"%(len(m.group(1))//3)
    return R if len(R)<30 else R[:27]+"..."
T=load(tm)
def sim(tape,p,s,cap,want=None,maxev=4,show=True):
    ev=[]
    for i in range(1,cap+1):
        r=tape.get(p,0)
        if s==6 and r==0:
            ks=[q for q in tape if tape[q]];lo,hi=min(ks),max(ks)
            L="".join(str(tape.get(q,0)) for q in range(lo,p));R="".join(str(tape.get(q,0)) for q in range(p+1,hi+1))
            ev.append((i,L,R))
            if want and i==want: return ev
            if not want and len(ev)>maxev: return ev
        t=T[(s,r)]
        if t is None: ev.append((i,"HALT",str(sum(tape.values()))));return ev
        tape[p]=t[0];p+=t[1];s=t[2]
    ev.append((cap,"CAP",""));return ev
def hand(L,R,cap=5000000,maxev=4):
    tape={}
    for i,ch in enumerate(L): tape[i-len(L)]=int(ch)
    for i,ch in enumerate(R): tape[i+1]=int(ch)
    return sim(tape,0,6,cap,maxev=maxev)
def show(e): return "HALT at step %d, %s ones"%(e[0],e[2]) if e[1]=="HALT" else "%s | %s"%(left(e[1]),right(e[2]))
def fate(L,cap=3000000):
    ev=hand(L,"101101",cap=cap,maxev=10**6);e=ev[-1]
    if e[1]=="HALT": return "HALT after %d gate visits, step %d"%(len(ev)-1,e[0])
    return "no halt in %d steps; last: %s"%(cap,show(ev[-2])[:70])
if __name__=="__main__":
    m=sys.argv[1]
    if m=="trace":
        N,a,b=map(int,sys.argv[2:5])
        for k,e in enumerate(sim({},0,0,N,maxev=b),1):
            if a<=k<=b: print("%9d  %s"%(e[0],show(e)))
    elif m=="depth":
        for x in range(1,15): print("x=%2d ->"%x,show(hand("11"+"10"*x+"1","101101",maxev=1)[1]))
    elif m=="gate":
        print("one counter c, then a working group of 6: the next three gate visits")
        for c in range(0,9): print(" c=%d :"%c," || ".join(show(e) for e in hand("1"+"110"+"10"*c+"1110"+"10"*6+"1","101101",maxev=3)[1:]))
        print("two counters d, c, then a working group of 2: run to the end")
        for d in (3,4,5):
            for c in (2,3,4,5): print(" d=%d c=%d :"%(d,c),fate("1"+"110"+"10"*d+"110"+"10"*c+"1110"+"10"*2+"1"))
