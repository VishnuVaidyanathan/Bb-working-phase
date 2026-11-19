"""passes.py TABLE FROM TO [slackcap] : cut a real run into passes (one picture per head turn) and print them as a story."""
import sys
tm=sys.argv[1];a=int(sys.argv[2]);b=int(sys.argv[3]);extra=int(sys.argv[4]) if len(sys.argv)>4 else 0
T={}
for s,x in enumerate(tm.split("_")):
    for k in (0,1):
        e=x[3*k:3*k+3];T[(s,k)]=None if e[2] in "Z-" else (int(e[0]),1 if e[1]=="R" else -1,ord(e[2])-65)
tape={};p=0;s=0;last=None;prev=None;names="SUVWXYZPQRT"
def cfg():
    ks=[q for q in tape if tape[q]]+[p];lo,hi=min(ks),max(ks)
    return names[s]+" "+"".join(("[%d]"%tape.get(q,0)) if q==p else str(tape.get(q,0)) for q in range(lo,hi+1))
print("slack 3\nmargin 2")
for i in range(1,b+1):
    t=T[(s,tape.get(p,0))]
    if t is None: break
    if i>=a and (prev is None or t[1]!=prev):
        c=cfg()
        if last: print(last[1],"->",c,i-last[0]+extra)
        last=(i,c)
    prev=t[1];tape[p]=t[0];p+=t[1];s=t[2]
