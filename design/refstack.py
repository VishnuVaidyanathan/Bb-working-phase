"""refstack.py : a loose reference stack machine for any numbers (as many states as it needs - NOT a candidate),
   used only to check the stack arithmetic (calc/stackcalc.py) against a real table.
   KL = cells written at home each round (a round adds K = KL + 1), m = size of a fresh store, RH = leftover that halts.
   The machine is run from a hand tape (block of b cells) and its tape is read each time the head is at home;
   the arithmetic is stepped one round at a time and must show the same block and stores every time."""
import sys
sys.path.insert(0,__file__.rsplit('/',2)[0]+'/calc')
def table(KL,m,RH):
    T={}
    hs=["H%d"%i for i in range(1,KL)]
    T[("A",0)]=(1,-1,hs[0]) if hs else (1,1,"B")
    for i,h in enumerate(hs): T[(h,0)]=(1,-1,hs[i+1]) if i+1<len(hs) else (1,1,"B")
    xs=["X%d"%i for i in range(1,m)]+["E"]
    T[("A",1)]=(1,1,xs[0])
    for i,x in enumerate(xs):
        left=(i+1) if x!="E" else 0
        if x!="E": T[(x,1)]=(1,1,xs[i+1])
        else: T[(x,1)]=(0,1,"B")
        T[(x,0)]=None if left==RH else (0,-1,"D")
    T[("B",0)]=(1,1,"C");T[("B",1)]=(1,1,"B");T[("C",0)]=(0,-1,"F");T[("C",1)]=(0,-1,"D")
    T[("D",0)]=(0,-1,"F");T[("D",1)]=(1,-1,"D");T[("F",0)]=(0,1,"A");T[("F",1)]=(1,-1,"F")
    return T
def as_text(T):
    names=sorted(set(s for s,_ in T),key=lambda s:(s!="A",s));L={n:chr(65+i) for i,n in enumerate(names)}
    def e(x): return "1RZ" if x is None else "%d%s%s"%(x[0],"R" if x[1]>0 else "L",L[x[2]])
    return "_".join(e(T.get((n,0),None) if (n,0) in T else None)+("---" if (n,1) not in T else e(T[(n,1)])) for n in names),len(names)
def machine_homes(T,b,maxsteps=3000000,maxhomes=400):
    """configs (block, stores) each time state A reads 0 (home, before the refill); ends with 'HALT' if it halts"""
    tape={i:1 for i in range(1,b+1)};p=0;s="A";out=[]
    for st in range(maxsteps):
        v=tape.get(p,0)
        if s=="A" and v==0:
            hi=max([k for k,x in tape.items() if x]+[p]);cells=[tape.get(i,0) for i in range(p+1,hi+2)]
            w=0
            while w<len(cells) and cells[w]: w+=1
            rest="".join(map(str,cells[w+1:]));stores=[len(x) for x in rest.split("0")] if rest else []
            while stores and stores[-1]==0: stores.pop()
            out.append((w,tuple(stores)))
            if len(out)>=maxhomes: return out
        e=T[(s,v)]
        if e is None: out.append("HALT");return out
        tape[p]=e[0];p+=e[1];s=e[2]
    return out
def model_homes(K,m,RH,b,maxhomes=400):
    """the arithmetic, one home visit at a time"""
    w=b;stores=[];out=[]
    while len(out)<maxhomes:
        while stores and stores[-1]==0: stores.pop()
        out.append((w,tuple(stores)))
        if stores and stores[0]>0: w+=K;stores[0]-=1;continue
        g=0
        while g<len(stores) and stores[g]==0: g+=1
        avail=w+K
        if stores and avail>m*g:
            d=stores[g];stores=[m]*(g-1)+[avail-m*g,d-1]+stores[g+1:];w=m
        else:
            k,r=divmod(avail,m)
            if r==RH: out.append("HALT");return out
            marks=[m]*k+([r] if r else [])
            w=marks[0];stores=marks[1:]+([0]*max(0,g-len(marks))+stores[g:] if stores else [])
    return out
if __name__=="__main__":
    bad=0;n=0
    for KL in (1,2,3,4):
        for m in (2,3,4):
            for RH in range(1,m):          # leftover 0 cannot be the halt in this layout: the hop over a store ends the same way
                T=table(KL,m,RH)
                for b in range(0,13):
                    a=machine_homes(T,b);c=model_homes(KL+1,m,RH,b,maxhomes=len(a) if a and a[-1]!="HALT" else 400)
                    k=min(len(a),len(c));n+=1
                    if a[:k]!=c[:k] or (a[-1]=="HALT")!=(c[-1]=="HALT" and len(c)<=len(a)):
                        bad+=1
                        if bad<=12:
                            i=next((i for i in range(k) if a[i]!=c[i]),k)
                            print("DIFFERENT: home +%d store %d halt-left %d first block %d at home visit %d: machine %s | arithmetic %s"%(KL,m,RH,b,i,a[max(0,i-1):i+2],c[max(0,i-1):i+2]))
    print("%d cases compared (machine tape at every home visit against the arithmetic), %d different"%(n,bad))
    print("example table, home +3, store 3, halt on 0 left:",as_text(table(3,3,0)))
def with_startup(KL,m,RH,b):
    """the reference table as text, with b start-up states in front that write a first block of b cells (for a simulator that starts blank)"""
    T=table(KL,m,RH);names=["P%d"%i for i in range(1,b+1)]+sorted(set(s for s,_ in T),key=lambda s:(s!="A",s))
    L={n:chr(65+i) for i,n in enumerate(names)}
    for i in range(1,b+1): T[("P%d"%i,0)]=(1,1,"P%d"%(i+1)) if i<b else (1,-1,"D")
    def e(n,v):
        if (n,v) not in T: return "---"
        x=T[(n,v)];return "1RZ" if x is None else "%d%s%s"%(x[0],"R" if x[1]>0 else "L",L[x[2]])
    return "_".join(e(n,0)+e(n,1) for n in names)
