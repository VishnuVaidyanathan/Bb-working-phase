"""follow.py TABLE a b w [steps] : start the table on  1^a 0 1^b [0] 1^w  in state A and list every time it is again on a tape of that shape in state A."""
import sys,re
tm=sys.argv[1];a,b,w=map(int,sys.argv[2:5]);N=int(sys.argv[5]) if len(sys.argv)>5 else 200000;T={}
for s,x in enumerate(tm.split("_")):
    for k in (0,1):
        e=x[3*k:3*k+3];T[(s,k)]=None if e[2] in "Z-" else (int(e[0]),1 if e[1]=="R" else -1,ord(e[2])-65)
cells=[1]*a+[0]+[1]*b;p=len(cells);cells+=[0]+[1]*w;tape={i:c for i,c in enumerate(cells) if c};s=0;out=[]
for i in range(N+1):
    if s==0 and tape.get(p,0)==0:
        ks=sorted(q for q in tape if tape[q])
        if ks:
            L="".join(str(tape.get(q,0)) for q in range(min(ks[0],p),p));R="".join(str(tape.get(q,0)) for q in range(p+1,max(ks[-1],p)+1))
            m=re.fullmatch(r'0*(1*)0(1*)',L) or re.fullmatch(r'0*()(1*)',L)
            if m and re.fullmatch(r'1*',R) and not (L.strip("0")=="" and False):
                out.append((i,len(m.group(1)),len(m.group(2)),len(R)))
    t=T[(s,tape.get(p,0))]
    if t is None: out.append((i,"HALT"));break
    if t[0]: tape[p]=1
    else: tape.pop(p,None)
    p+=t[1];s=t[2]
print(tm," ".join(("(%d,%d,%d)"%o[1:]) if len(o)==4 else "HALT@%d"%o[0] for o in out[:28]))
