"""signature.py FILE [STEPS] : for each machine (lines "LABEL TABLE"), run from a blank tape and print its road signature:
   wires used, roads used, digits with 1 / 2 / 3 digits before them, digits with only one digit after them,
   pure pipes (one in, one out), one-wire loops, and which digits lead into the halt's state."""
import sys
H="0123456789abcd"
def sig(tm,NS):
    T={};n=len(tm.split("_"));halt=None
    for s,x in enumerate(tm.split("_")):
        for k in (0,1):
            e=x[3*k:3*k+3]
            if e[2] in "Z-":
                T[(s,k)]=None
                if e[2]=="Z": halt=(s,k)
            else: T[(s,k)]=(int(e[0]),1 if e[1]=="R" else -1,ord(e[2])-65)
    tape={};p=0;s=0;prev=None;c=set();steps=0;halted=False
    for i in range(NS):
        r=tape.get(p,0);d=2*s+r
        if prev is not None: c.add((prev,d))
        prev=d;t=T[(s,r)];steps+=1
        if t is None: halted=True;break
        if t[0]: tape[p]=1
        else: tape.pop(p,None)
        p+=t[1];s=t[2]
    used=sorted(set(a for a,b in c)|set(b for a,b in c))
    ins={d:sorted(a for a,b in c if b==d) for d in used};outs={d:sorted(b for a,b in c if a==d) for d in used}
    g=lambda k,m:"".join(H[d] for d in used if len(m[d])==k) or "-"
    pipes="".join(H[d] for d in used if len(ins[d])==1 and len(outs[d])==1) or "-"
    loops="".join(H[d] for d in used if d in outs[d]) or "-"
    hd="-"
    if halt:
        feeders=[H[2*q+k] for (q,k),t in T.items() if t and t[2]==halt[0] and (2*q+k) in used]
        hd="%s after %s"%(H[2*halt[0]+halt[1]],"".join(sorted(feeders)))
    return dict(states=n,wires=len([d for d in used if T[(d//2,d%2)] is not None]),roads=len(c),in1=g(1,ins),in2=g(2,ins),in3=g(3,ins)+g(4,ins).replace("-",""),out1=g(1,outs),pipes=pipes,loops=loops,halt=hd,done="halted at %d"%steps if halted else "")
if __name__=="__main__":
    NS=int(sys.argv[2]) if len(sys.argv)>2 else 3000000
    print("label | states | wires | roads | before: one | two | three+ | after: one | pipes | one-wire loops | halt")
    for line in open(sys.argv[1]):
        if not line.strip(): continue
        lab,tm=line.split()[:2];r=sig(tm,NS)
        print(" | ".join(str(x) for x in (lab,r["states"],r["wires"],r["roads"],r["in1"],r["in2"],r["in3"],r["out1"],r["pipes"],r["loops"],r["halt"],r["done"])))
