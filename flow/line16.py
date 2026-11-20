"""line16.py TABLE [STEPS] : line 16 of the scorecard - does a ticket walk a whole block?
   At each rare road (used 5 to 300 times) the tape is folded (1^n, (10)^n, (1100)^n ...).  Over 4 or more visits in a row
   (every visit, every 2nd or every 3rd) with the same tape shape, each folded number is followed:
     BLOCK   = it multiplies (each step at least x1.4)        COUNTER = it drops by the same amount each time
   Line 16 passes when one road shows a BLOCK and a COUNTER together (two stores: a ticket from the counter multiplies the block).
   Prints the best road found.  check(tm,NS) -> (passes, text)."""
import sys,re
from collections import Counter,defaultdict
H="0123456789abcd"
def table(tm):
    T={}
    for s,x in enumerate(tm.split("_")):
        for k in (0,1):
            e=x[3*k:3*k+3];T[(s,k)]=None if e[2] in "Z-" else (int(e[0]),1 if e[1]=="R" else -1,ord(e[2])-65)
    return T
def fold(x):
    for w in ("1100","1000","100","110","10","01","1"):
        x=re.sub(r'(?:%s){4,}'%w,lambda m:" %s^%d "%(("("+w+")") if len(w)>1 else w,len(m.group(0))//len(w)),x)
    return x
def run(tm,NS,want=None,cap=90):
    T=table(tm);N=2000000;tape=bytearray(2*N);p=N;s=0;lo=hi=N;prev=-1;c=Counter();snaps=defaultdict(list)
    for i in range(NS):
        r=tape[p];d=2*s+r
        if want is None: c[(prev,d)]+=1
        elif (prev,d) in want and len(snaps[(prev,d)])<cap:
            snaps[(prev,d)].append((i,fold(tape[lo:p].decode('latin1').translate({0:'0',1:'1'}))+" [%d] "%r+fold(tape[p+1:hi+1].decode('latin1').translate({0:'0',1:'1'}))))
        t=T[(s,r)]
        if t is None: break
        tape[p]=t[0];p+=t[1];s=t[2];prev=d
        if p<lo: lo=p
        if p>hi: hi=p
        if p<5 or p>2*N-5: break
    return c if want is None else snaps
def kinds(v):
    if all(b>=1.4*a and a>0 for a,b in zip(v,v[1:])): return "BLOCK"
    dif={b-a for a,b in zip(v,v[1:])}
    if len(dif)==1 and dif.pop()<0: return "COUNTER"
    return ""
def check(tm,NS=10000000,HI=300):
    c=run(tm,NS);want={k for k,n in c.items() if 5<=n<=HI and k[0]>=0}
    snaps=run(tm,NS,want);best=None
    for rd,L in snaps.items():
        for st in (1,2,3):
            for off in range(st):
                seq=L[off::st];sh=[re.sub(r'\^\d+','^#',x[1]) for x in seq];i=0
                while i<len(seq):
                    j=i
                    while j+1<len(seq) and sh[j+1]==sh[i]: j+=1
                    if j-i+1>=4:
                        nums=[[int(n) for n in re.findall(r'\^(\d+)',x[1])] for x in seq[i:j+1]]
                        cols=list(zip(*nums));ks=[kinds(v) for v in cols]
                        sc=(("BLOCK" in ks)+("COUNTER" in ks),j-i+1)
                        if "BLOCK" in ks and (best is None or sc>best[0]):
                            best=(sc,rd,st,[(k,list(v)[:8]) for k,v in zip(ks,cols) if k],sh[i])
                    i=j+1
    if best is None: return False,"no road shows a multiplying block over 4 visits"
    sc,rd,st,cols,shape=best;ok=sc[0]==2
    txt="road %s>%s, every %s visit, %d visits | "%(H[rd[0]],H[rd[1]],{1:"",2:"2nd",3:"3rd"}[st],sc[1])+" ; ".join("%s %s"%(k,",".join(map(str,v))) for k,v in cols)
    return ok,txt+("" if ok else "  (a block but no counter: one store)")
if __name__=="__main__":
    ok,txt=check(sys.argv[1],int(sys.argv[2]) if len(sys.argv)>2 else 10000000);print("PASS" if ok else "FAIL",txt)
