"""gatelog.py TABLE [STEPS] : run a 7-state table from a blank tape and, each time the gate state G is entered,
   print the step and the tape as run lengths.  Thought tool only."""
import sys
t=sys.argv[1];n=int(sys.argv[2]) if len(sys.argv)>2 else 3000000
rows=t.split("_");T={}
for q,r in enumerate(rows):
    for b in (0,1):
        e=r[b*3:b*3+3];T[(q,b)]=None if e[2] in "-Z" else (int(e[0]),1 if e[1]=="R" else -1,ord(e[2])-65)
tape={};pos=0;st=0
def fold():
    ks=sorted(k for k,v in tape.items() if v)
    if not ks: return "(blank)"
    lo,hi=ks[0],ks[-1];q=lo;o=[]
    while q<=hi:
        a=0
        while tape.get(q,0): a+=1;q+=1
        z=0
        while q<=hi and not tape.get(q,0): z+=1;q+=1
        w=str(a)+"_"*(z-1)
        if o and o[-1][0]==w: o[-1][1]+=1
        else: o.append([w,1])
    return " ".join(w if k==1 else "%sx%d"%(w,k) for w,k in o)[:100]
c=0
for k in range(n):
    v=tape.get(pos,0);e=T[(st,v)]
    if e is None: print("HALT at step",k,"ones",sum(tape.values()),"|",fold());break
    tape[pos]=e[0];pos+=e[1]
    if e[2]==6 and st!=6:
        c+=1
        if c<=40: print("G entry %d at step %d (wire %s%d): %s"%(c,k,"ABCDEFG"[st],v,fold()))
    st=e[2]
else: print("still running after",n,"steps; G entered",c,"times |",fold())
