"""fromtape.py TABLE STATE LEFT RIGHT [STEPS] : run a table from a chosen tape instead of a blank one (for thought experiments only -
   a machine still counts only from a blank tape).  LEFT and RIGHT are 0/1 strings; the head starts on the first cell of RIGHT.
   Prints the folded digits, the end tape, and the roads used.  run(...) returns (digits, tape string, halted)."""
import sys,re
H="0123456789abcd"
def run(tm,state,left,right,NS=200000,stop=None):
    T={}
    for s,x in enumerate(tm.split("_")):
        for k in (0,1):
            e=x[3*k:3*k+3];T[(s,k)]=None if e[2] in "Z-" else (int(e[0]),1 if e[1]=="R" else -1,ord(e[2])-65)
    tape={};
    for i,c in enumerate(left): tape[i-len(left)]=int(c)
    for i,c in enumerate(right): tape[i]=int(c)
    lo0=-len(left);hi0=len(right)-1
    p=0;s=ord(state)-65;D=[];halt=False
    for i in range(NS):
        r=tape.get(p,0);D.append(H[2*s+r]);t=T[(s,r)]
        if t is None: halt=True;break
        tape[p]=t[0];p+=t[1];s=t[2]
        if stop and stop(p,lo0,hi0,i): break
    ks=[k for k,v in tape.items() if v]+[p];lo=min(ks);hi=max(ks)
    ts="".join(("[%d]"%tape.get(q,0)) if q==p else str(tape.get(q,0)) for q in range(lo,hi+1))
    return "".join(D),ts,halt
if __name__=="__main__":
    from digits import fold
    d,t,h=run(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],int(sys.argv[5]) if len(sys.argv)>5 else 200000)
    print(fold(d));print(t[:300]);print("HALT" if h else "no halt")
