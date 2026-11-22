"""lists.py TABLE STEPS STATE [FROM] [MAX]: the tape as a list of counters at each far-right turn made in STATE.
   n = n words `10` in a row, | = `100`, # = `1000`, % = `10000`; other runs are written a.b ; the last lone 1 is dropped."""
import sys
sys.argv[0]
import os
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"view.py")).read().split("t=sys.argv[1]")[0])
def tok(w):
    out=[];i=0
    while i<len(w):
        if w[i]==(1,1):
            j=i
            while j<len(w) and w[j]==(1,1): j+=1
            out.append(str(j-i));i=j
        else:
            out.append({(1,2):"|",(1,3):"#",(1,4):"%"}.get(w[i],"%d.%d"%w[i]));i+=1
    return " ".join(out)
t=sys.argv[1];n=int(sys.argv[2]);HS=ord(sys.argv[3])-65;frm=int(sys.argv[4]) if len(sys.argv)>4 else 0;mx=int(sys.argv[5]) if len(sys.argv)>5 else 80
T=parse(t);tape={};pos=0;st=0;lo=hi=0;last=None;k=0
for s in range(n):
    v=tape.get(pos,0)
    if v==0 and pos==hi and st==HS:
        w=words(tape,lo,hi)
        if w and w[-1][1]: w[-1]=(w[-1][0],0)
        if w and w[-1]==(1,0): w=w[:-1]
        f=tok(w)
        if f!=last:
            k+=1;last=f
            if k>frm: print("%9d  %s"%(s,f[:170]))
            if k>=frm+mx: break
    e=T[(st,v)]
    if e is None: print("HALT",s);break
    tape[pos]=e[0];pos+=e[1];st=e[2];lo=min(lo,pos);hi=max(hi,pos)
