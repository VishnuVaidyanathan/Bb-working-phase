"""transcript.py TABLE BLOCK STORE [STORE ...] : run a table on a hand tape (block, one empty cell, store, ...; head on the empty cell
   left of the block, first state) and print the transcript in Vishnu's digits (A0=0 A1=1 B0=2 B1=3 ... ; 10=a 11=b 12=c 13=d),
   repeats folded as 3x4, one line per visit to the far-left empty cell, with the tape as run lengths.  Thought tool only."""
import sys
D="0123456789abcd"
def run(t,cfg,n=5000,maxlines=12):
    rows=t.split("_");T={}
    for q,r in enumerate(rows):
        for b in (0,1):
            e=r[b*3:b*3+3];T[(q,b)]=None if e[2] in "-Z" else (int(e[0]),1 if e[1]=="R" else -1,ord(e[2])-65)
    cells=[]
    for a in cfg: cells+=[1]*a+[0]
    tape={i+1:v for i,v in enumerate(cells) if v};pos=0;st=0;seq=[];lines=0
    def shape():
        lo=min([k for k,v in tape.items() if v],default=0);hi=max([k for k,v in tape.items() if v],default=0);out=[];q=lo
        while q<=hi:
            a=0
            while tape.get(q,0): a+=1;q+=1
            z=0
            while q<=hi and not tape.get(q,0): z+=1;q+=1
            out.append(str(a)+"_"*(z-1))
        return " ".join(out)
    def fold(s):
        o=[];
        for d in s:
            if o and o[-1][0]==d: o[-1][1]+=1
            else: o.append([d,1])
        return " ".join(d if k==1 else "%sx%d"%(d,k) for d,k in o)
    print("start:",shape())
    for k in range(n):
        v=tape.get(pos,0)
        if v==0 and pos<=min([q for q,x in tape.items() if x],default=0)-1 and seq:
            print("  ",fold(seq),"  ->",shape());seq=[];lines+=1
            if lines>=maxlines: return
        e=T[(st,v)]
        if e is None: print("  ",fold(seq+[D[st*2+v]]),"  -> STOP on wire",D[st*2+v],"(",rows[st][v*3:v*3+3],")",shape());return
        seq.append(D[st*2+v]);tape[pos]=e[0];pos+=e[1];st=e[2]
if __name__=="__main__": run(sys.argv[1],[int(x) for x in sys.argv[2:]])
