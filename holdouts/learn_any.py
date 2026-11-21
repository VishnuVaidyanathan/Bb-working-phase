"""learn_any.py TABLE [STEPS] : read any machine of the `10`-counter kind as a token list at its visits to the right end, and list the
   kinds of step between two visits (the end of the list before -> after).  Tokens: a number = that many words `10`; "|" = `100`;
   anything else is written ones.zeros."""
import sys
from collections import defaultdict,Counter
sys.path.insert(0,__file__.rsplit('/',2)[0]+'/pavel')
import look,words
def dec(ws):
    out=[];i=0
    while i<len(ws):
        if ws[i]==(1,1):
            j=i
            while j<len(ws) and ws[j]==(1,1): j+=1
            out.append(j-i);i=j
        elif ws[i]==(1,2): out.append("|");i+=1
        else:
            a,b=ws[i];out.append("%d.%d"%(a,b));i+=1
    return out
def build(tokens):
    cells=[]
    for t in tokens:
        if isinstance(t,int): cells+=[1,0]*t
        elif t=="|": cells+=[1,0,0]
        else:
            a,b=map(int,t.split("."));cells+=[1]*a+[0]*b
    if not cells or cells[-1]==1: cells.append(0)
    return {i:1 for i,v in enumerate(cells) if v},len(cells)-1
def visits(tm,n,tape=None,pos=0,state="A",maxv=10**9,side="R"):
    T=look.parse(tm);tape=dict(tape or {});st=state;lo=min(list(tape)+[pos]);hi=max(list(tape)+[pos]);out=[];first=True
    for step in range(n):
        v=tape.get(pos,0)
        if v==0 and (pos==hi if side=="R" else pos==lo) and not first:
            out.append((step,st,dec(words.words(tape,lo,hi))))
            if len(out)>=maxv: break
        first=False
        e=T[(st,v)]
        if e is None: out.append((step,"HALT",[]));break
        tape[pos]=e[0];pos+=e[1];st=e[2];lo=min(lo,pos);hi=max(hi,pos)
    return out
def pack(c):
    out=[];i=0
    while i<len(c):
        j=i
        while j<len(c) and c[j]==c[i]=="|": j+=1
        if j-i>1: out.append("|x%d"%(j-i));i=j
        else: out.append(str(c[i]));i+=1
    return " ".join(out)
def home_state(v): return Counter(st for s,st,c in v if st!="HALT").most_common(1)[0][0]
if __name__=="__main__":
    tm=sys.argv[1];n=int(sys.argv[2]) if len(sys.argv)>2 else 3000000
    side=sys.argv[4] if len(sys.argv)>4 else "R"
    v=visits(tm,n,side=side);hs=home_state(v)
    if side=="L":                      # the work is at the left end: read the list from the left, i.e. reversed
        v=[(s,st,c[::-1]) for s,st,c in v]
    seq=[c for s,st,c in v if st==hs]
    print("visits at the %s end:"%side,"(list shown with the working end last)" if side=="L" else "");print("visits: %d, of which in state %s: %d; last: %s"%(len(v),hs,len(seq),pack(seq[-1])[:110]))
    inst=defaultdict(list)
    for a,b in zip(seq,seq[1:]):
        i=0
        while i<len(a) and i<len(b) and a[i]==b[i]: i+=1
        i=max(0,i-1)
        inst[tuple("n" if isinstance(x,int) else x for x in a[i:])].append((a[i:],b[i:]))
    print(len(inst),"kinds of step")
    for key,lst in sorted(inst.items(),key=lambda kv:-len(kv[1]))[:int(sys.argv[3]) if len(sys.argv)>3 else 30]:
        ex=[];seen=set()
        for a,b in lst:
            kb=tuple("n" if isinstance(x,int) else x for x in b)
            if kb in seen and len(ex)>=2: continue
            seen.add(kb);ex.append("%s -> %s"%(pack(a),pack(b)))
            if len(ex)>=3: break
        print("%5d [%s]  e.g. %s"%(len(lst)," ".join(key)," ;; ".join(ex))[:230])
