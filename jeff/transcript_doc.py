"""transcript_doc.py [STEPS] : Jeff Ketchersid's champion from a blank tape, as digits, a new line at each firing of digit 0 (home) and after each digit behind the door (c or d),
   repeats folded (3x7), with the step number and the tape after the line (run lengths; _ = one more empty cell; 2_x3 = three such runs).
   Thought tool; credit for the machine: Jeff Ketchersid."""
import sys
from collections import Counter
t="1RB0RG_1RC1RB_0RD1RZ_0LE0LD_0LF1LE_1RA1LF_1LC0RB";D="0123456789abcd";N=int(sys.argv[1]) if len(sys.argv)>1 else 3000
rows=t.split("_");T={}
for q,r in enumerate(rows):
    for b in (0,1):
        e=r[b*3:b*3+3];T[(q,b)]=None if e[2]=="Z" else (int(e[0]),1 if e[1]=="R" else -1,ord(e[2])-65)
def fold(s):
    o=[]
    for d in s:
        if o and o[-1][0]==d: o[-1][1]+=1
        else: o.append([d,1])
    return " ".join(d if k==1 else "%sx%d"%(d,k) for d,k in o)
def shape():
    ks=[k for k,v in tape.items() if v]
    if not ks: return "(blank)"
    lo,hi=min(ks),max(ks);o=[];q=lo
    while q<=hi:
        a=0
        while tape.get(q,0): a+=1;q+=1
        z=0
        while q<=hi and not tape.get(q,0): z+=1;q+=1
        w=str(a)+"_"*(z-1)
        if o and o[-1][0]==w: o[-1][1]+=1
        else: o.append([w,1])
    return " ".join(w if k==1 else "%sx%d"%(w,k) for w,k in o)
tape={};pos=0;st=0;seq=[];use=Counter();line=0
for k in range(N+1):
    v=tape.get(pos,0);d=D[st*2+v]
    if (d=="0" and seq) or k==N or (seq and seq[-1] in "cd"):
        line+=1;print("%3d  %5d  %-34s %s"%(line,k,fold(seq),shape()));seq=[]
        if k==N: break
    e=T[(st,v)];seq.append(d);use[d]+=1;tape[pos]=e[0];pos+=e[1];st=e[2]
print("USE "+" ".join("%s:%d"%(d,use[d]) for d in D))
