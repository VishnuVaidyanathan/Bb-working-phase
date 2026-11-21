"""words.py [STEPS] [EVENT] : Pavel Kropitz's machine; tape read as words when the head is at the left edge.
   A word is a run of 1s with the 0s after it, written ones.zeros ; repeated words are counted:  (1.1)x6 (2.1)x3 ...
   A visit = the head arrives from the right on a 0 with no 1 left of it. EVENT can limit it to given state-symbols (default: any)."""
import sys,look
def words(tape,lo,hi):
    out=[];i=lo
    while i<=hi and not tape.get(i,0): i+=1
    while i<=hi:
        a=0
        while tape.get(i,0): a+=1;i+=1
        b=0
        while i<=hi and not tape.get(i,0): b+=1;i+=1
        out.append((a,b))
    return out
def pack(ws):
    out=[];i=0
    while i<len(ws):
        j=i
        while j<len(ws) and ws[j]==ws[i]: j+=1
        a,b=ws[i];name="%d.%d"%(a,b) if b else "%d"%a
        out.append(name if j-i==1 else "(%s)x%d"%(name,j-i));i=j
    return " ".join(out)
def visits(n,events=("any",),tm=look.P,maxv=10**9):
    T=look.parse(tm);tape={};pos=0;st="A";lo=hi=0;out=[];left=0;came=0      # left = number of 1s left of the head
    for step in range(n):
        v=tape.get(pos,0)
        if left==0 and v==0 and came<0 and (events==("any",) or (st+str(v)) in events):
            out.append((step,st+str(v),words(tape,lo,hi)))
            if len(out)>=maxv: break
        e=T[(st,v)]
        if e is None: out.append((step,"HALT",words(tape,lo,hi)));break
        tape[pos]=e[0]
        if e[1]>0: left+=e[0]
        else: left-=tape.get(pos-1,0)
        pos+=e[1];st=e[2];came=e[1]
        lo=min(lo,pos);hi=max(hi,pos)
    return out
if __name__=="__main__":
    n=int(sys.argv[1]) if len(sys.argv)>1 else 200000
    ev=tuple(sys.argv[2].split(",")) if len(sys.argv)>2 else ("any",)
    for step,e,ws in visits(n,ev)[:int(sys.argv[3]) if len(sys.argv)>3 else 120]: print("%9d %s  %s"%(step,e,pack(ws)[:150]))
