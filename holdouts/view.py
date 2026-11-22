"""view.py TABLE STEPS [SIDE] [MAXLINES]: the tape as run lengths each time the head turns at the far end (SIDE R or L) on a 0.
   A run of 1s of length a followed by b zeros is written a.b ; a word repeated k times is written (a.b)^k."""
import sys
def parse(t):
    T={}
    for q,r in enumerate(t.split("_")):
        for b in (0,1):
            e=r[b*3:b*3+3];T[(q,b)]=None if e[2] in "-Z" else (int(e[0]),1 if e[1]=="R" else -1,ord(e[2])-65)
    return T
def words(tape,lo,hi):
    out=[];q=lo
    while q<=hi and not tape.get(q,0): q+=1
    while q<=hi:
        a=0
        while q<=hi and tape.get(q,0): a+=1;q+=1
        b=0
        while q<=hi and not tape.get(q,0): b+=1;q+=1
        out.append((a,b))
    return out
def fmt(w):
    s=[];i=0
    while i<len(w):
        j=i
        while j<len(w) and w[j]==w[i]: j+=1
        x="%d.%d"%w[i] if i<len(w)-1 or w[i][1] else "%d"%w[i][0]
        s.append(x if j-i==1 else "(%s)^%d"%(x,j-i));i=j
    return " ".join(s)
t=sys.argv[1];n=int(sys.argv[2]);side=sys.argv[3] if len(sys.argv)>3 else "R";mx=int(sys.argv[4]) if len(sys.argv)>4 else 60
T=parse(t);tape={};pos=0;st=0;lo=hi=0;last=None;k=0;use={}
for s in range(n):
    v=tape.get(pos,0)
    if v==0 and ((side=="R" and pos==hi) or (side=="L" and pos==lo)):
        w=words(tape,lo,hi)
        if w and w[-1][1]: w[-1]=(w[-1][0],0)
        f=fmt(w)
        if f!=last:
            print("%8d %s  %s"%(s,chr(65+st),f[:150]));last=f;k+=1
            if k>=mx: break
    e=T[(st,v)]
    use[(st,v)]=use.get((st,v),0)+1
    if e is None: print("HALT",s);break
    tape[pos]=e[0];pos+=e[1];st=e[2];lo=min(lo,pos);hi=max(hi,pos)
print("wire use:"," ".join("%s%d:%d"%(chr(65+q),b,c) for (q,b),c in sorted(use.items())))
