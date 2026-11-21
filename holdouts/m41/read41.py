"""read41.py : one of Polygon's undecided 7-state holdouts, read as words at each visit to the right end.
   Machine M41 = 1RB0LC_1LA1LE_0RD---_1LB1RE_0LA1LF_0RD0RG_0LD1RF  (halt = state C reading 1).  List credit: Polygon, Discord BB community."""
import sys
sys.path.insert(0,__file__.rsplit('/',3)[0]+'/pavel')
import look,words
M="1RB0LC_1LA1LE_0RD---_1LB1RE_0LA1LF_0RD0RG_0LD1RF"
def visits(n,tm=M,maxv=10**9,tape=None,pos=0,state="A"):
    T=look.parse(tm);tape=dict(tape or {});st=state;lo=min(list(tape)+[pos]);hi=max(list(tape)+[pos]);out=[]
    for step in range(n):
        v=tape.get(pos,0)
        if v==0 and pos==hi and step>0:
            out.append((step,st,tuple(words.words(tape,lo,hi))))
            if len(out)>=maxv: break
        e=T[(st,v)]
        if e is None: out.append((step,"HALT",()));break
        tape[pos]=e[0];pos+=e[1];st=e[2];lo=min(lo,pos);hi=max(hi,pos)
    return out
if __name__=="__main__":
    n=int(sys.argv[1]) if len(sys.argv)>1 else 3000
    for step,st,ws in visits(n)[:int(sys.argv[2]) if len(sys.argv)>2 else 60]: print("%8d %s %s"%(step,st,words.pack(ws)[:150]))
