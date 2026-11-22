"""squeeze_tapes.py ROOMYFILE [MINSTATES] : squeeze a roomy table using hand-made tapes (one-cell layout, home = first state on the blank
   cell left of the block) to see which wires are used.  Tries groupings into fewer and fewer states and checks each squeezed table
   against the roomy one, step for step, on every tape.  Prints, for each number of states, how many groupings work and one table."""
import sys,squeeze as S
TAPES=[(5,[2,4,3]),(7,[0,4,3]),(7,[0,5,3]),(6,[0,0,4,3]),(6,[0,0,6,4]),(4,[0,0,5,4]),(3,[2,2,2,6])]
def load(f):
    rows=[l.split()[:3] for l in open(f) if l.strip() and not l.startswith("#")]
    return "_".join(r[1]+r[2] for r in rows),[r[0] for r in rows]
def start(cfg):
    cells=[0]+[1]*cfg[0]
    for s in cfg[1]: cells+=[0]+[1]*s
    return {i:1 for i,v in enumerate(cells) if v}
def run(T,W,p,cfg,n=300000,u=None):
    tape=start(cfg);pos=0;st=0;g=p[0] if p else 0
    for k in range(n):
        v=tape.get(pos,0);e=T[st][v]
        if u is not None: u.add((st,v))
        if W is not None:
            f=W.get((g,v))
            if e is None or e=="HALT": return f is not None and f[0]=="H" if e=="HALT" else True
            if f is None or f[0]=="H" or (f[0],f[1])!=(e[0],e[1]) or f[2]!=p[e[2]]: return False
            g=f[2]
        elif e is None or e=="HALT": return True
        tape[pos]=e[0];pos+=1 if e[1]=="R" else -1;st=e[2]
    return True
if __name__=="__main__":
    t,names=load(sys.argv[1]);lowest=int(sys.argv[2]) if len(sys.argv)>2 else 7
    T=S.parse(t);u=set()
    for cfg in TAPES: run(T,None,None,cfg,u=u)
    for s in range(len(T)):
        for b in (0,1):
            if T[s][b]=="HALT": u.add((s,b))
    print("roomy table:",len(T),"states;",len(u),"wires used on",len(TAPES),"hand-made tapes")
    for k in range(len(T)-1,lowest-1,-1):
        res=S.squeeze(T,u,k);good=[(p,W) for p,W in res if all(run(T,W,p,cfg) for cfg in TAPES)]
        print("into %d states: %d groupings, %d run exactly like the roomy table"%(k,len(res),len(good)))
        if good:
            p,W=good[0];groups={}
            for i,g in enumerate(p): groups.setdefault(g,[]).append(names[i])
            print("    e.g. states merged:"," ".join("".join(v) for v in groups.values() if len(v)>1) or "-","| table:",S.table(W,k,p[0]))
        else: break
