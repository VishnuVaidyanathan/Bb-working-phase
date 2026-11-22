"""look.py TABLE [STEPS] : run a table on hand-made tapes (and from a blank tape) and print the tape as run lengths
   each time the head stands on the blank cell at the far left (any state).  a_ means a run followed by 2 empty cells, a__ by 3."""
import sys
def parse(t):
    T={}
    for q,r in enumerate(t.split("_")):
        for b in (0,1):
            e=r[b*3:b*3+3];T[(q,b)]=None if e[2] in "-Z" else (int(e[0]),1 if e[1]=="R" else -1,ord(e[2])-65)
    return T
def run(t,cfg,start,n=300000,maxl=40,every=False):
    T=parse(t);cells=[]
    for i,a in enumerate(cfg): cells+=[1]*a+([0] if i<len(cfg)-1 else [])
    tape={i+1:v for i,v in enumerate(cells) if v};pos=0;st=ord(start)-65;lo=0;hi=len(cells);out=[];last=None
    for k in range(n):
        v=tape.get(pos,0)
        if v==0 and pos<=lo:
            runs=[];q=lo
            while q<=hi:
                a=0
                while q<=hi and tape.get(q,0): a+=1;q+=1
                z=0
                while q<=hi and not tape.get(q,0): z+=1;q+=1
                if a: runs.append(str(a)+("_"*(z-1) if q<=hi else ""))
            s=" ".join(runs)
            key=tuple(runs[1:]) if not every else s
            if key!=last:
                last=key
                if len(out)<maxl: out.append("%d %s: %s"%(k,chr(65+st),s[:110]))
        e=T[(st,v)]
        if e is None: out.append("HALT at step %d on %s%d, ones %d"%(k,chr(65+st),v,sum(tape.values())));return out
        tape[pos]=e[0];pos+=e[1];st=e[2];lo=min(lo,pos);hi=max(hi,pos)
    out.append("still running after %d steps, ones %d"%(n,sum(tape.values())));return out
if __name__=="__main__":
    t=sys.argv[1]
    for cfg,st in (([3,6],"D"),([3,7],"D"),([3,4,3],"D"),([3,2,2,2],"D"),([],"A")):
        print(cfg,"start",st);print("   "+"\n   ".join(run(t,cfg,st)))
