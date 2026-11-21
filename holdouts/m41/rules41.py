"""rules41.py : thought experiments on M41.  A tape is built from a list of tokens in its own coding and run from a D visit.
   Tokens: a number n = n words `10` (a counter);  "|" = the word `100` (separator; "|xk" = k of them);  "1.3" = `1000`;  "1.4" = `10000`."""
import sys,read41 as R
sys.path.insert(0,__file__.rsplit('/',3)[0]+'/pavel')
import look,words
def dec(ws):
    out=[];i=0
    while i<len(ws):
        if ws[i]==(1,1):
            j=i
            while j<len(ws) and ws[j]==(1,1): j+=1
            out.append(j-i);i=j
        elif ws[i]==(1,2):
            j=i
            while j<len(ws) and ws[j]==(1,2): j+=1
            out+=["|"]*(j-i);i=j
        else:
            a,b=ws[i];out.append("%d.%d"%(a,b) if b else "%d"%a);i+=1
    return out
def build(tokens):
    cells=[]
    for t in tokens:
        if isinstance(t,int): cells+=[1,0]*t
        elif t=="|": cells+=[1,0,0]
        else:
            a,b=map(int,t.split("."));cells+=[1]*a+[0]*b
    return {i:1 for i,v in enumerate(cells) if v},len(cells)-1
def run(tokens,maxsteps=3000000,maxv=10**9,want="D"):
    tape,pos=build(tokens)
    v=R.visits(maxsteps,tape=tape,pos=pos,state="D",maxv=maxv)
    return [(s,st,dec(ws)) for s,st,ws in v]
def pack(c):
    out=[];i=0
    while i<len(c):
        j=i
        while j<len(c) and c[j]==c[i]=="|": j+=1
        if j-i>1: out.append("|x%d"%(j-i));i=j
        else: out.append(str(c[i]));i+=1
    return " ".join(out)
def shapes(tokens,maxsteps=3000000,limit=14):
    out=[];prev=None
    for s,st,c in run(tokens,maxsteps):
        if st=="HALT": out.append("HALT");break
        if st!="D": continue
        key=tuple("n" if isinstance(x,int) else x for x in c)
        if key!=prev: out.append(pack(c))
        prev=key
        if len(out)>=limit: break
    return out
if __name__=="__main__":
    real=[(s,c) for s,st,c in [(s,st,dec(ws)) for s,st,ws in R.visits(400000)] if st=="D"]
    ok=0
    for (s,a),(s2,b) in zip(real[60:260],real[61:261]):
        r=[c for _,st,c in run(a,maxsteps=200000,maxv=6) if st=="D"]
        ok+= (len(r)>0 and r[0]==b)
    print("builder check: %d of 200 real D-visit steps reproduced"%ok)
    for toks in ([2,"|","|","|","1.3",2,"|",1,"|",2,"|"],[2,"|","|","1.3",0,"|",3,"|",2,"|"],[2,"|","|","1.3","|",5,"|",2,"|"],[2,"|","1.3","|",5,"|",2,"|"],[2,"1.3","|",5,"|",2,"|"]):
        print("start:",pack(toks));print("   ->"," ; ".join(shapes(toks))[:700])
