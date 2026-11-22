"""squeeze.py TABLE [TARGET] [STEPS] :  (write the halt wire as 1RZ and a wire with no job as ---)
   the "squeeze" step of  story -> trips -> roomy table -> SQUEEZE -> check.
   A roomy table has one state per job and may have many states.  Two states can be made one if, for each symbol, the wires that are
   actually USED agree (same write, same move, same next state after merging); a wire that is never used is free.
   The tool: runs the table from a blank tape for STEPS steps to see which wires are used, tries every way of grouping the states into
   TARGET groups (default 7), keeps the groupings with no clash, and checks each squeezed table against the roomy one step by step
   (same symbol written, same move, at every step).  Prints the squeezed tables in tree normal form.  Nothing is proved beyond STEPS."""
import sys
def parse(t):
    T=[]
    for r in t.split("_"):
        row=[]
        for b in (0,1):
            e=r[b*3:b*3+3];row.append(None if e[2]=="-" else ("HALT" if e[2]=="Z" else (int(e[0]),e[1],ord(e[2])-65)))
        T.append(row)
    return T
def used_wires(T,n):
    tape={};pos=0;st=0;u=set()
    for k in range(n):
        v=tape.get(pos,0);u.add((st,v));e=T[st][v]
        if e is None or e=="HALT": return u,k
        tape[pos]=e[0];pos+=1 if e[1]=="R" else -1;st=e[2]
    return u,None
def partitions(n,k):
    # all ways to put states 0..n-1 into exactly k groups (restricted growth strings)
    a=[0]*n
    def rec(i,m):
        if i==n:
            if m==k: yield a[:]
            return
        if n-i < k-m: return
        for g in range(min(m+1,k)):
            a[i]=g
            yield from rec(i+1,max(m,g+1))
    yield from rec(1,1)
def squeeze(T,u,k):
    n=len(T);out=[]
    for p in partitions(n,k):
        W={};ok=True
        for (s,b) in u:
            e=T[s][b];val=("H",) if (e is None or e=="HALT") else (e[0],e[1],p[e[2]])
            key=(p[s],b)
            if key in W and W[key]!=val: ok=False;break
            W[key]=val
        if ok: out.append((p,W))
    return out
def table(W,k,start):
    # tree normal form: states named in order of first use from a blank tape, first move to the right
    def run(mirror):
        tape={};pos=0;st=start;order=[st]
        for i in range(200000):
            v=tape.get(pos,0);e=W.get((st,v))
            if e is None or e[0]=="H": break
            d=e[1] if not mirror else ("L" if e[1]=="R" else "R")
            tape[pos]=e[0];pos+=1 if d=="R" else -1;st=e[2]
            if st not in order: order.append(st)
        return order
    first=W.get((start,0));mirror=bool(first and first[0]!="H" and first[1]=="L")
    order=run(mirror);order+=[g for g in range(k) if g not in order];new={g:i for i,g in enumerate(order)}
    rows=[]
    for g in order:
        s=""
        for b in (0,1):
            e=W.get((g,b))
            if e is None: s+="---"
            elif e[0]=="H": s+="1RZ"
            else: s+="%d%s%s"%(e[0],(e[1] if not mirror else ("L" if e[1]=="R" else "R")),chr(65+new[e[2]]))
        rows.append(s)
    return "_".join(rows)
def same_run(T,W,p,n):
    tape={};pos=0;st=0;g=p[0]
    for k in range(n):
        v=tape.get(pos,0);e=T[st][v];f=W.get((g,v))
        if e is None or e=="HALT": return f is not None and f[0]=="H"
        if f is None or f[0]=="H" or (f[0],f[1])!=(e[0],e[1]) or f[2]!=p[e[2]]: return False
        tape[pos]=e[0];pos+=1 if e[1]=="R" else -1;st=e[2];g=f[2]
    return True
if __name__=="__main__":
    t=sys.argv[1];k=int(sys.argv[2]) if len(sys.argv)>2 else 7;n=int(sys.argv[3]) if len(sys.argv)>3 else 2000000
    T=parse(t);u,h=used_wires(T,n)
    for s_ in range(len(T)):
        for b_ in (0,1):
            if T[s_][b_]=="HALT": u.add((s_,b_))      # the halt wire is always kept, used or not
    print("roomy table: %d states, %d of %d wires used in %s"%(len(T),len(u),2*len(T),("%d steps (it halts)"%h) if h is not None else "%d steps"%n))
    res=squeeze(T,u,k);good=[(p,W) for p,W in res if same_run(T,W,p,n)]
    print("groupings into %d states with no clash: %d ; of those that run exactly like the roomy table: %d"%(k,len(res),len(good)))
    seen=set()
    for p,W in good:
        s=table(W,k,p[0])
        if s not in seen: seen.add(s);print("  ",s,"  groups:","".join(chr(65+x) for x in p))
