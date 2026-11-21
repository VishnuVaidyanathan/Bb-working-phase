import sys
def nb(t):
    rows=t.replace("1RZ","---").split("_");cells=[r[i:i+3] for r in rows for i in (0,3)]
    out=set()
    for i,c in enumerate(cells):
        opts=[w+d+s for w in "01" for d in "LR" for s in "ABCDEFG"]
        for o in opts:
            if o==c: continue
            cc=cells[:];cc[i]=o
            if c!="---":       # keep exactly one halt wire
                out.add("_".join(cc[2*k]+cc[2*k+1] for k in range(7)))
            else:              # the halt wire moves: every other cell becomes the halt in turn
                for j in range(14):
                    if j==i: continue
                    c2=cc[:];c2[j]="---";out.add("_".join(c2[2*k]+c2[2*k+1] for k in range(7)))
    return sorted(out)
for t in sys.argv[1:]:
    for x in nb(t): print(x)
