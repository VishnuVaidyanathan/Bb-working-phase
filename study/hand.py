"""Run a machine from a hand-made tape and list the tape at each use of chosen digits."""
import sys,re
from read import load,tapestr,D
def run(tm,left,state,head,right,watch,cap=2000000,maxev=6):
    T=load(tm);tape={}
    for i,ch in enumerate(left): tape[i-len(left)]=int(ch)
    tape[0]=head
    for i,ch in enumerate(right): tape[i+1]=int(ch)
    p=0;s=state;out=[]
    for i in range(cap):
        r=tape.get(p,0);d=D[2*s+r]
        if i>0 and d in watch:
            out.append("%s: %s"%(d,tapestr(tape,p)))
            if len(out)>=maxev: break
        t=T[(s,r)]
        if t is None: out.append("HALT at %d (ones %d)"%(i+1,sum(tape.values())+1)); break
        tape[p]=t[0];p+=t[1];s=t[2]
    else: out.append("...")
    return out
