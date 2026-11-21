import sys
sys.path.insert(0,"/home/claude/bb-working-phase/holdouts")
import gate_test as G
tm=sys.argv[1];n=int(sys.argv[2]);T=G.parse(tm);HS=sys.argv[3]
v,h=G.visits(T,n,keep=10**9)
def tok(runs):
    out=[];
    for (a,b),k in runs:
        if (a,b)==(1,1): out.append(str(k))
        else:
            s={(1,2):"|",(1,3):"#"}.get((a,b),"%d.%d"%(a,b))
            out+= [s]*k
    return " ".join(out)
prev=None;shown=0
for step,st,side,runs,gap in v:
    if side!="R" or "ABCDEFG"[st]!=HS: continue
    s=tok(runs);shape="".join(ch if not ch.isdigit() else "n" for ch in s)
    import re
    shape=re.sub("n+","n",shape)
    if shape!=prev:
        print(step,s[:170]);shown+=1;prev=shape
    if shown>=int(sys.argv[4]): break
print("halt",h,"visits",len(v))
