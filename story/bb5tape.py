"""bb5tape.py "TAPE" [events] [TABLE]: start the BB(5) champion's table (or TABLE) in state A on the bracketed cell of a hand-made tape,
   and print the tape every time it starts cutting (digit pair 46: the wall) and when it halts.  Blocks of 1s and pieces are folded."""
import sys,re
tape_s=sys.argv[1];ne=int(sys.argv[2]) if len(sys.argv)>2 else 12
tm=sys.argv[3] if len(sys.argv)>3 else "1RB1LC_1RC1RB_1RD0LE_1LA1LD_1RZ0LA";T={}
for s,x in enumerate(tm.split("_")):
    for k in (0,1):
        e=x[3*k:3*k+3];T[(s,k)]=None if e[2] in "Z-" else (int(e[0]),1 if e[1]=="R" else -1,ord(e[2])-65)
cells=[];p=0
for ch in tape_s.replace(" ",""):
    if ch=="[": p=len(cells)
    elif ch in "01": cells.append(int(ch))
tape={i for i,c in enumerate(cells) if c};s=0;prev=None;ev=0
def show():
    lo=min(min(tape),p);hi=max(max(tape),p)
    x="".join(("[%d]"%(q in tape)) if q==p else ("1" if q in tape else "0") for q in range(lo,hi+1))
    x=re.sub(r'1{5,}',lambda m:" 1^%d "%len(m.group(0)),x)
    for w in ("0001","001","01"):
        x=re.sub(r'(?:%s){3,}'%w,lambda m:" (%s)^%d "%(w,len(m.group(0))//len(w)),x)
    return x
print("start     ",show())
for i in range(1,2*10**8):
    b=1 if p in tape else 0;d=2*s+b
    if prev==4 and d==6:
        ev+=1;print("wall %-3d %9d  %s"%(ev,i,show()))
        if ev>=ne: break
    prev=d;t=T[(s,b)]
    if t is None: print("HALT at step %d, ones %d   %s"%(i,len(tape)+1,show()));break
    if t[0]: tape.add(p)
    else: tape.discard(p)
    p+=t[1];s=t[2]
