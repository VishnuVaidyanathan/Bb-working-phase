"""rows.py : does the row-of-21 holdout make row after row?  Start it on a small lone counter "c #" (state E, right end) and list
   every later visit where the list is again one lone counter, and the row made from it."""
import sys,re
sys.path.insert(0,"/home/claude/bb-working-phase/holdouts")
import gate_test as G
T=G.parse("1RB0LG_1RC0RA_1LD1LE_1LB0LC_0LF0RE_0LG0LC_0RA---")
def tok(runs):
    out=[]
    for (a,b),k in runs:
        if (a,b)==(1,1): out.append(str(k))
        else: out+=[{(1,2):"|",(1,3):"#"}.get((a,b),"%d.%d"%(a,b))]*k
    return out
def go(c,n):
    cells=[1,0]*c+[1,0,0,0];tape={i:1 for i,v in enumerate(cells) if v};pos=len(cells)-1;st=4;lo=0;hi=pos;ev=[]
    for s in range(n):
        v=tape.get(pos,0)
        if st==4 and v==0 and pos==hi:
            t=tok(G.runs_of(tape,lo,hi))
            if len(t)==2 and t[1]=="#": ev.append("step %d: lone counter %s"%(s,t[0]))
            elif t[0]=="1" and set(t[1:-1])=={"|"} and t[-1]=="#": ev.append("step %d: row of %d bars"%(s,len(t)-2))
        e=T[(st,v)]
        if e is None: ev.append("HALT at %d"%s);break
        tape[pos]=e[0];pos+=e[1];st=e[2];lo=min(lo,pos);hi=max(hi,pos)
    return ev
for c in (1,2,3):
    print("start: lone counter",c);[print("   ",e) for e in go(c,int(sys.argv[1]))]
