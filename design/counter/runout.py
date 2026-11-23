"""runout.py TABLE WARM KEEP [STEPS] : what does a counter machine do when its counter runs out?
   Runs TABLE from a blank tape for WARM steps, then cuts the third run of 1s (the small counter that goes down by 1) to KEEP cells
   by removing cells and closing the tape up, and runs on.  Prints the tape as run lengths whenever the number of runs changes
   or the counter run changes, and says if it halts.  Hand-made tape after the cut: this is a look, not a run from blank."""
import sys
t=sys.argv[1];warm=int(sys.argv[2]);keep=int(sys.argv[3]);more=int(sys.argv[4]) if len(sys.argv)>4 else 3000000
rows=t.split("_");T={}
for q,r in enumerate(rows):
    for b in (0,1):
        e=r[b*3:b*3+3];T[(q,b)]=None if e[2] in "-Z" else (int(e[0]),1 if e[1]=="R" else -1,ord(e[2])-65)
tape={};pos=0;st=0
def runs():
    ks=sorted(k for k,v in tape.items() if v);out=[];
    if not ks: return []
    lo,hi=ks[0],ks[-1];q=lo
    while q<=hi:
        a=0;s=q
        while tape.get(q,0): a+=1;q+=1
        z=0
        while q<=hi and not tape.get(q,0): z+=1;q+=1
        out.append((s,a,z))
    return out
def show(): return " ".join(str(a)+"_"*(z-1) for s,a,z in runs())[:120]
for k in range(warm):
    v=tape.get(pos,0);e=T[(st,v)];tape[pos]=e[0];pos+=e[1];st=e[2]
R=runs();print("after",warm,"steps:",show(),"| head in run-area at",pos,"state","ABCDEFGH"[st])
s,a,z=R[2];cut=a-keep
new={}
for k,v in tape.items():
    if not v: continue
    if k<s+keep: new[k]=1
    elif k>=s+a: new[k-cut]=1
tape=new
if pos>=s+keep: pos=max(s+keep,pos-cut)
print("counter cut to",keep,":",show(),"| head at",pos)
last=None
for k in range(more):
    v=tape.get(pos,0);e=T[(st,v)]
    if e is None: print("HALT after",k,"more steps; ones",sum(tape.values()),"|",show());break
    tape[pos]=e[0];pos+=e[1];st=e[2]
    if k%2000==0:
        R=runs();key=(len(R),R[2][1] if len(R)>2 else -1)
        if key!=last: last=key;print("  +%d: %s"%(k,show()))
else: print("still running after",more,"more steps:",show())
