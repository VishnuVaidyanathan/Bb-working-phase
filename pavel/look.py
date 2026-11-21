"""look.py : Pavel Kropitz's earlier BB(7) champion, tape read as runs at chosen moments (credit for the machine: Pavel Kropitz)."""
import sys
P="1RB0RA_1LC1LF_1RD0LB_1RA1LE_1RZ0LC_1RG1LD_0RG0RF"
def parse(t):
    T={}
    for q,row in enumerate(t.split('_')):
        for b in (0,1):
            e=row[b*3:b*3+3];T[(chr(65+q),b)]=None if e[2] in 'Z-' else (int(e[0]),1 if e[1]=='R' else -1,e[2])
    return T
def rl(tape,lo,hi,pos=None):
    out=[];i=lo
    while i<=hi:
        v=tape.get(i,0);j=i
        while j<=hi and tape.get(j,0)==v: j+=1
        seg="%d^%d"%(v,j-i) if j-i>1 else str(v)
        if pos is not None and i<=pos<j: seg="["+seg+"]"
        out.append(seg);i=j
    return " ".join(out)
def run(tm,n,when):
    T=parse(tm);tape={};pos=0;st="A";lo=hi=0;out=[]
    for step in range(n):
        v=tape.get(pos,0)
        if when(st,v,pos,lo,hi): out.append((step,st,v,rl(tape,lo,hi,pos)))
        e=T[(st,v)]
        if e is None: out.append((step,"HALT",v,rl(tape,lo,hi,pos)));break
        tape[pos]=e[0];pos+=e[1];st=e[2]
        lo=min(lo,pos);hi=max(hi,pos)
    return out
if __name__=="__main__":
    n=int(sys.argv[1]) if len(sys.argv)>1 else 20000
    which=sys.argv[2] if len(sys.argv)>2 else "edge"
    if which=="edge": w=lambda st,v,pos,lo,hi: pos==hi and v==0 or pos==lo and v==0
    else: w=lambda st,v,pos,lo,hi,s=which[0],b=int(which[1]): st==s and v==b
    for step,st,v,t in run(P,n,w)[:int(sys.argv[3]) if len(sys.argv)>3 else 80]: print("%8d %s%d %s"%(step,st,v,t[:170]))
