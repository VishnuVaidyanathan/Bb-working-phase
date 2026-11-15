"""Transcript workbench.  Give a draft transcript; get the tables that support it from a blank tape,
or the place where no table can follow it.
   digits 0-9 a-d (2*state + symbol read),  x(n) = n copies,  ? = any digit,  spaces are ignored.
   python3 draft.py "0 2468bb a1d 2468b a1 c47698b a1 c47698a03" """
import sys,re
sys.setrecursionlimit(100000)
D="0123456789abcd"
def expand(s):
    s=re.sub(r"\s+","",s)
    s=re.sub(r"(.)\((\d+)\)",lambda m:m.group(1)*int(m.group(2)),s)
    return s
def fit(target):
    sols=[];best=[0]
    def ok(i,k): return target[i]=='?' or target[i]==D[k]
    def go(i,tape,p,s,tab):
        while i<len(target):
            r=tape.get(p,0)
            if not ok(i,2*s+r): best[0]=max(best[0],i); return
            if (s,r) not in tab:
                for w in (0,1):
                    for m in (1,-1):
                        if i==0 and m<0: continue          # first move to the right (mirror images dropped)
                        if i+1<len(target) and target[i+1]!='?': qs=[D.index(target[i+1])//2]
                        else: qs=range(7)
                        for q in qs:
                            t2=dict(tab);t2[(s,r)]=(w,m,q);tp=dict(tape);tp[p]=w
                            go(i+1,tp,p+m,q,t2)
                return
            w,m,q=tab[(s,r)];tape[p]=w;p+=m;s=q;i+=1
        best[0]=len(target); sols.append(tab)
    go(0,{},0,0,{})
    return sols,best[0]
def show(tab): return "_".join("".join((str(tab[(s,r)][0])+("R" if tab[(s,r)][1]>0 else "L")+"ABCDEFG"[tab[(s,r)][2]]) if (s,r) in tab else "---" for r in range(2)) for s in range(7))
if __name__=="__main__":
    t=expand(sys.argv[1]); S,b=fit(t)
    print("draft: %d digits, %d different wires"%(len(t),len(set(t)-{'?'})))
    if not S: print("no table supports it.  It can be followed up to digit %d:  %s | %s"%(b,t[:b],t[b:b+12]))
    else:
        u=sorted(set(show(x) for x in S)); print("%d tables support it"%len(u))
        for x in u[:20]: print("  ",x)
