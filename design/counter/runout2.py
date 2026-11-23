"""runout2.py TABLE WARM KEEP TAIL [STEPS] : as runout.py, and also the far row of single cells (the slow counter) is cut:
   only the last TAIL runs of it are kept (or TAIL = runs:1,1 gives the row by hand; runs: alone = no row).  Shows what the machine does when BOTH counters run out.
   Hand-made tape after the cut: a look, not a run from blank."""
import sys
t=sys.argv[1];warm=int(sys.argv[2]);keep=int(sys.argv[3]);tailarg=sys.argv[4];tail=int(tailarg) if not tailarg.startswith("runs:") else 0;more=int(sys.argv[5]) if len(sys.argv)>5 else 3000000
rows=t.split("_");T={}
for q,r in enumerate(rows):
    for b in (0,1):
        e=r[b*3:b*3+3];T[(q,b)]=None if e[2] in "-Z" else (int(e[0]),1 if e[1]=="R" else -1,ord(e[2])-65)
tape={};pos=0;st=0
def runs():
    ks=sorted(k for k,v in tape.items() if v);out=[]
    if not ks: return []
    lo,hi=ks[0],ks[-1];q=lo
    while q<=hi:
        a=0;s=q
        while tape.get(q,0): a+=1;q+=1
        z=0
        while q<=hi and not tape.get(q,0): z+=1;q+=1
        out.append((s,a,z))
    return out
def fold(R):
    o=[]
    for s,a,z in R:
        w=str(a)+"_"*(z-1)
        if o and o[-1][0]==w: o[-1][1]+=1
        else: o.append([w,1])
    return " ".join(w if k==1 else "%sx%d"%(w,k) for w,k in o)[:110]
for k in range(warm):
    v=tape.get(pos,0);e=T[(st,v)];tape[pos]=e[0];pos+=e[1];st=e[2]
R=runs();print("after",warm,"steps:",fold(R))
cells=[]
keepruns=R[:3]+R[len(R)-tail:] if tail<len(R)-3 else R
if tailarg.startswith("runs:"):
    keepruns=R[:3]+[(0,int(a),1) for a in tailarg[5:].split(",") if a]
base=R[0][0];x=base;headnew=None
for j,(s,a,z) in enumerate(keepruns):
    if j==2: a=keep
    for i in range(a): cells.append(x);x+=1
    x+=z if z else 1
# head: keep it at the same offset inside the first runs if it was there, else at the left end
off=pos-base
tape={c:1 for c in cells};pos=base+min(off,R[0][1]) if off<=R[0][1] else base-1
print("cut            :",fold(runs()),"| head at offset",pos-base,"state","ABCDEFGH"[st])
last=None
for k in range(more):
    v=tape.get(pos,0);e=T[(st,v)]
    if e is None: print("HALT after",k,"more steps; ones",sum(tape.values()),"|",fold(runs()));break
    tape[pos]=e[0];pos+=e[1];st=e[2]
    if k%4000==0:
        R=runs();key=(len(R),)
        if key!=last: last=key;print("  +%d: %s"%(k,fold(R)))
else: print("still running after",more,"more steps:",fold(runs()))
