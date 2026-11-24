"""transcript_million.py [STEPS] : Jeff Ketchersid's champion from a blank tape as digits only.
   A digit repeated 3 or more times in a row is folded (3x40); nothing else is compressed.
   A new line starts at each digit 0 (home) and after each digit behind the door (c or d).  Credit for the machine: Jeff Ketchersid."""
import sys
t="1RB0RG_1RC1RB_0RD1RZ_0LE0LD_0LF1LE_1RA1LF_1LC0RB";D="0123456789abcd";N=int(sys.argv[1]) if len(sys.argv)>1 else 1000000
rows=t.split("_");T={}
for q,r in enumerate(rows):
    for b in (0,1):
        e=r[b*3:b*3+3];T[(q,b)]=None if e[2]=="Z" else (int(e[0]),1 if e[1]=="R" else -1,ord(e[2])-65)
def fold(s):
    o=[]
    for d in s:
        if o and o[-1][0]==d: o[-1][1]+=1
        else: o.append([d,1])
    return " ".join(d if k==1 else (d+" "+d if k==2 else "%sx%d"%(d,k)) for d,k in o)
tape={};pos=0;st=0;seq=[]
for k in range(N+1):
    v=tape.get(pos,0);d=D[st*2+v]
    if (d=="0" and seq) or k==N or (seq and seq[-1] in "cd"):
        print(fold(seq));seq=[]
        if k==N: break
    e=T[(st,v)];seq.append(d);tape[pos]=e[0];pos+=e[1];st=e[2]
