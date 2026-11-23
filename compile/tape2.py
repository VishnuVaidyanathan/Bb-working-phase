"""tape2.py TABLE GAP BLOCK STORE [STORE ...] : as transcript.py but the runs are separated by GAP empty cells.
   Head on the empty cell left of the block, first state.  Prints the transcript in Vishnu's digits, one line per visit of
   digit 0 (A0), with the tape as run lengths (each _ = one more empty cell).  Unset wires are written ---.  Thought tool only."""
import sys
D="0123456789abcd"
def run(t,gap,cfg,n=20000,maxlines=14):
    rows=t.split("_");T={}
    for q,r in enumerate(rows):
        for b in (0,1):
            e=r[b*3:b*3+3];T[(q,b)]=None if e[2] in "-Z" else (int(e[0]),1 if e[1]=="R" else -1,ord(e[2])-65)
    cells=[]
    for a in cfg: cells+=[1]*a+[0]*gap
    tape={i+1:v for i,v in enumerate(cells) if v};pos=0;st=0;seq=[];lines=0
    def shape():
        ks=[k for k,v in tape.items() if v]
        if not ks: return "(blank)"
        lo,hi=min(ks),max(ks);out=[];q=lo
        while q<=hi:
            a=0
            while tape.get(q,0): a+=1;q+=1
            z=0
            while q<=hi and not tape.get(q,0): z+=1;q+=1
            out.append(str(a)+"_"*(z-1))
        return " ".join(out)
    def fold(s):
        o=[]
        for d in s:
            if o and o[-1][0]==d: o[-1][1]+=1
            else: o.append([d,1])
        return " ".join(d if k==1 else "%sx%d"%(d,k) for d,k in o)
    print("start:",shape())
    for k in range(n):
        v=tape.get(pos,0);d=D[st*2+v]
        if d=="0" and seq:
            print("  ",fold(seq)[:150],"  ->",shape()[:60]);seq=[];lines+=1
            if lines>=maxlines: return
        e=T[(st,v)]
        if e is None: print("  ",fold(seq+[d])[:150],"  -> STOP on digit",d,"|",shape()[:60]);return
        seq.append(d);tape[pos]=e[0];pos+=e[1];st=e[2]
    print("  ",fold(seq)[:150],"  -> (no more home visits) |",shape()[:60])
if __name__=="__main__": run(sys.argv[1],int(sys.argv[2]),[int(x) for x in sys.argv[3:]])
