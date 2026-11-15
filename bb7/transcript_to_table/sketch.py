"""Sketch workbench: from an imagined transcript to tables.
   Write the blocks you imagine; the tool lists every table that can play them from a blank tape.
     digits 0-9 a-d  = 2*state + symbol read          x+   = a run of x, any length (1 or more)
     x(n)            = exactly n copies               ?    = any one digit      spaces are ignored
   python3 sketch.py "0 2 5 8 b+ a 1 d 2 4 7+ 6 9 8 a 0 3+ 2 5 9+ 8 a 0 3+" """
import sys,re
sys.setrecursionlimit(100000)
D="0123456789abcd"
def tokens(s):
    s=re.sub(r"\s+","",s); s=re.sub(r"(.)\((\d+)\)",lambda m:m.group(1)*int(m.group(2)),s)
    out=[];i=0
    while i<len(s):
        if i+1<len(s) and s[i+1]=='+': out.append((s[i],True)); i+=2
        else: out.append((s[i],False)); i+=1
    return out
def fit(tok,cap=5000,limit=2000):
    sols=[];best=[0]
    def go(i,inrun,tape,p,s,tab,n):
        # i = index of the token being matched; inrun = True if token i is a run that has started
        while True:
            if i==len(tok) or (i==len(tok)-1 and inrun):
                best[0]=len(tok)
                if len(sols)<limit: sols.append(dict(tab))
                return
            if n>cap: return
            r=tape.get(p,0); d=D[2*s+r]
            c,plus=tok[i]
            if inrun and d!=c:                      # the run is over: this digit must start the next token
                i+=1; inrun=False; continue
            if c!='?' and d!=c: best[0]=max(best[0],i); return
            if (s,r) not in tab:
                for w in (0,1):
                    for m in (1,-1):
                        if n==0 and m<0: continue
                        for q in range(7):
                            t2=dict(tab);t2[(s,r)]=(w,m,q);tp=dict(tape);tp[p]=w
                            go(i if plus else i+1, plus, tp,p+m,q,t2,n+1)
                return
            w,m,q=tab[(s,r)];tape[p]=w;p+=m;s=q;n+=1
            if plus: inrun=True
            else: i+=1
    go(0,False,{},0,0,{},0)
    return sols,best[0]
def show(tab): return "_".join("".join((str(tab[(s,r)][0])+("R" if tab[(s,r)][1]>0 else "L")+"ABCDEFG"[tab[(s,r)][2]]) if (s,r) in tab else "---" for r in range(2)) for s in range(7))
if __name__=="__main__":
    tok=tokens(sys.argv[1]); S,b=fit(tok)
    print("sketch: %d blocks, %d different wires"%(len(tok),len(set(c for c,_ in tok)-{'?'})))
    u=sorted(set(show(x) for x in S))
    if not u: print("no table can play it.  It can be followed up to block %d:  %s | %s"%(b," ".join(c+("+" if p else "") for c,p in tok[:b])," ".join(c+("+" if p else "") for c,p in tok[b:b+6])))
    else:
        print("%d tables can play it"%len(u))
        for x in u[:25]: print("  ",x)
