"""lone.py : what the row-of-21 holdout does with a lone counter "M #" (state E at the right end), for M = 1, 2, 3, ...
   Prints the list at every visit of E to the right end until a row of bars stands (or 40 visits)."""
import sys
sys.path.insert(0,"/home/claude/bb-working-phase/holdouts")
import gate_test as G
T=G.parse("1RB0LG_1RC0RA_1LD1LE_1LB0LC_0LF0RE_0LG0LC_0RA---")
def tok(runs):
    out=[]
    for (a,b),k in runs:
        if (a,b)==(1,1): out.append(str(k))
        else: out+=[{(1,2):"|",(1,3):"#"}.get((a,b),"%d.%d"%(a,b))]*k
    return out
def go(c,n,maxv):
    cells=[1,0]*c+[1,0,0,0];tape={i:1 for i,v in enumerate(cells) if v};pos=len(cells)-1;st=4;lo=0;hi=pos;ev=[];left0=0
    for s in range(n):
        v=tape.get(pos,0)
        if st==4 and v==0 and pos==hi:
            t=tok(G.runs_of(tape,lo,hi));ev.append((s," ".join(t), min(k for k in tape if tape[k]) if any(tape.values()) else 0))
            if len(ev)>1 and (len(t)>2 and set(t[1:-1])=={"|"} and t[-1]=="#" and t[0].isdigit()): break
            if len(ev)>=maxv: break
        e=T[(st,v)]
        if e is None: ev.append((s,"HALT",0));break
        tape[pos]=e[0];pos+=e[1];st=e[2];lo=min(lo,pos);hi=max(hi,pos)
    return ev
for c in range(1,int(sys.argv[1])+1):
    ev=go(c,2000000,int(sys.argv[2]))
    print("M =",c,": ", "  ->  ".join(x[1] for x in ev)[:400], "   (steps %d, left edge moved %d)"%(ev[-1][0],-ev[-1][2]))
