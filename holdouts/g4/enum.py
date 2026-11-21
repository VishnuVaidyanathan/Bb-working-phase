import sys,itertools
sys.path.insert(0,"/home/claude/bb-working-phase/holdouts")
import gate_test as G
tm="1RB0LG_1RC0RA_1LD1LE_1LB0LC_0LF0RE_0LG0LC_0RA---";T=G.parse(tm)
def cells(toks):
    c=[]
    for t in toks:
        if t=="|": c+=[1,0,0]
        elif t=="#": c+=[1,0,0,0]
        else: c+=[1,0]*t
    return c
def run(toks,n=200000):
    c=cells(toks);tape={i:1 for i,v in enumerate(c) if v};pos=len(c)-1;st=4
    # E visit: head on last (fresh) cell: the visit is recorded with head at hi reading 0
    for s in range(n):
        e=T[(st,tape.get(pos,0))]
        if e is None: return s
        tape[pos]=e[0];pos+=e[1];st=e[2]
    return None
# check against a real visit: "20 #"  must not halt
print("real 20 #:",run([20,"#"]),"  real 1 | | #:",run([1,"|","|","#"]))
res=[]
# lists: counters and separators alternate freely; end with '#'
for L in range(1,6):
    for body in itertools.product([0,1,2,3,4,5,"|","#"],repeat=L):
        ok=True
        for a,b in zip(body,body[1:]):
            if isinstance(a,int) and isinstance(b,int): ok=False
        if not ok or 0 in body and False: continue
        body=[x for x in body if x!=0] if False else list(body)
        if 0 in body: continue
        toks=body+["#"]
        h=run(toks,60000)
        if h is not None: res.append((len(toks),h,toks))
res.sort(key=lambda r:(r[0],r[1]))
print(len(res),"halting small lists")
rest=[r for r in res if r[2][-2:]!=["#","#"]]
print(len(rest),"that do not end in # #")
for L,h,t in rest[:40]: print(h," ".join(map(str,t)))
