"""homes.py TABLE "blocks" w [n] : start on  1^c 0 1^c ... [0] 1^w  (blocks = sizes left to right, e.g. 2,1,0) in state A;
   print the tape each time the machine is back in state A reading 0 with a 0-free block to its right (a 'home')."""
import sys,re
tm=sys.argv[1];bl=[int(x) for x in sys.argv[2].split(",")];w=int(sys.argv[3]);n=int(sys.argv[4]) if len(sys.argv)>4 else 30;T={}
for s,x in enumerate(tm.split("_")):
    for k in (0,1):
        e=x[3*k:3*k+3];T[(s,k)]=None if e[2] in "Z-" else (int(e[0]),1 if e[1]=="R" else -1,ord(e[2])-65)
cells=[]
for i,c in enumerate(bl): cells+=[1]*c+([0] if i<len(bl)-1 else [])
p=len(cells);cells+=[0]+[1]*w;tape={i:1 for i,c in enumerate(cells) if c};s=0;out=[];last=None
for i in range(2000000):
    if s==0 and p not in tape:
        ks=sorted(tape)
        if ks:
            L="".join("1" if q in tape else "0" for q in range(min(ks[0],p),p));R="".join("1" if q in tape else "0" for q in range(p+1,max(ks[-1],p)+1))
            if re.fullmatch(r'1*',R):
                d=[len(x) for x in L.split("0")] if L else []
                key=(tuple(d),len(R))
                if key!=last: out.append("(%s | %d)"%(",".join(map(str,d)),len(R)));last=key
                if len(out)>=n: break
    t=T.get((s,1 if p in tape else 0))
    if t is None: out.append("HALT");break
    if t[0]: tape[p]=1
    else: tape.pop(p,None)
    p+=t[1];s=t[2]
    if abs(p)>3000: out.append("RUNS AWAY");break
print(" ".join(out))
