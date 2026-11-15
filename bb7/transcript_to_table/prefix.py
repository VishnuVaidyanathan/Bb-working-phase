import sys
sys.setrecursionlimit(100000)
D="0123456789abcd"
def champ(n):
    tm="1RB0RG_1RC1RB_0RD1RZ_0LE0LD_0LF1LE_1RA1LF_1LC0RB".split('_')
    T={(s,r):(int(tm[s][3*r]),1 if tm[s][3*r+1]=='R' else -1,ord(tm[s][3*r+2])-65) for s in range(7) for r in range(2)}
    tape={};p=0;s=0;out=""
    for i in range(n):
        r=tape.get(p,0);out+=D[2*s+r];w,m,q=T[(s,r)];tape[p]=w;p+=m;s=q
    return out
def count(target):
    # all tables (write, move, next free) whose run from blank gives exactly these digits
    sols=[]
    def go(i,tape,p,s,tab):
        while i<len(target):
            r=tape.get(p,0)
            if D[2*s+r]!=target[i]: return
            if (s,r) not in tab:
                # next state is forced by the next digit if there is one
                for w in (0,1):
                    for m in (1,-1):
                        qs=[int(target[i+1],16)//2] if i+1<len(target) else range(7)
                        for q in qs:
                            t2=dict(tab);t2[(s,r)]=(w,m,q);tp=dict(tape);tp[p]=w
                            go(i+1,tp,p+m,q,t2)
                return
            w,m,q=tab[(s,r)];tape[p]=w;p+=m;s=q;i+=1
        sols.append(tab)
    go(0,{},0,0,{})
    return sols
full=champ(400)
for n in (10,17,26,30,34,35,36,40,50,69,141,319):
    S=count(full[:n])
    wires=len(set(full[:n]))
    print("first %3d digits: %2d wires seen, %4d tables fit"%(n,wires,len(S)))
S=count(full[:36])
def show(tab): return "_".join("".join((str(tab[(s,r)][0])+("R" if tab[(s,r)][1]>0 else "L")+"ABCDEFG"[tab[(s,r)][2]]) if (s,r) in tab else "---" for r in range(2)) for s in range(7))
for t in S[:6]: print(show(t))
