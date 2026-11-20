"""play.py : run a table from a hand-made tape (thought experiment) and print the stores each time it is back at rest
   (rest = the start state, on a blank cell, left of everything).  stores are printed as lengths of the blocks of 1, with the zeros between when not one."""
import re,sys
def tab(tm):
    T={}
    for s,x in enumerate(tm.split("_")):
        for k in (0,1):
            e=x[3*k:3*k+3];T[(s,k)]=None if e[2] in "Z-" else (int(e[0]),1 if e[1]=="R" else -1,ord(e[2])-65)
    return T
def stores(t):
    out=[];
    for m in re.finditer(r'(1+)(0*)',t):
        out.append(str(len(m.group(1)))+("" if len(m.group(2))<=1 else "_"*(len(m.group(2))-1)))
    return " ".join(out)
def play(tm,S,blocks,NS=2000000,maxshow=40):
    T=tab(tm);right='0'+'0'.join('1'*b for b in blocks);tape={i:int(c) for i,c in enumerate(right)};p=0;s=ord(S)-65;s0=s;out=[];last=None;lo=0;hi=len(right)
    for i in range(NS):
        r=tape.get(p,0)
        if p<lo: lo=p
        if p>hi: hi=p
        if s==s0 and r==0 and not any(tape.get(q,0) for q in range(lo,p)) and tape.get(p+1,0)==1:
            ks=[k for k in range(p,hi+1) if tape.get(k,0)]
            t=stores("".join(str(tape.get(q,0)) for q in range(min(ks),max(ks)+1)))
            if t!=last: out.append(t);last=t
            if len(out)>=maxshow: break
        t=T[(s,r)]
        if t is None: out.append("STOPS on unused wire %s%d at step %d, ones %d"%(chr(65+s),r,i,sum(tape.values())));break
        tape[p]=t[0];p+=t[1];s=t[2]
        if abs(p)>200000: out.append("runs away");break
    else: out.append("…")
    return out
if __name__=="__main__":
    tm,S=sys.argv[1],sys.argv[2];print(" | ".join(play(tm,S,[int(x) for x in sys.argv[3].split(',')])))
