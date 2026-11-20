"""homes.py [STEPS] : Jeff Ketchersid's BB(7) champion read at every home visit (state A reading 0), from a blank tape.
   The tape right of the head is written as runs:  ones.zeros ones.zeros ...   (first number = block, then the gap after it, and so on).
   Used to read his rules off his own tape (thought tool; credit for the machine: Jeff Ketchersid)."""
import sys
J="1RB0RG_1RC1RB_0RD1RZ_0LE0LD_0LF1LE_1RA1LF_1LC0RB"
def parse(t):
    T={}
    for q,row in enumerate(t.split('_')):
        for b in (0,1):
            e=row[b*3:b*3+3];T[(chr(65+q),b)]=None if e[2] in 'Z-' else (int(e[0]),1 if e[1]=='R' else -1,e[2])
    return T
def homes(tm,maxsteps,tape=None,pos=0,state="A",maxhomes=10**9):
    T=parse(tm);tape=dict(tape or {});st=state;out=[];hi=max(list(tape)+[0]);lo=0
    for step in range(maxsteps):
        v=tape.get(pos,0)
        if st=="A" and v==0:
            runs=[];q=pos+1
            while q<=hi+1:
                a=0
                while tape.get(q,0): a+=1;q+=1
                b=0
                while q<=hi+1 and not tape.get(q,0): b+=1;q+=1
                runs.append((a,b))
            if runs and runs[-1][0]==0: runs.pop()
            left=sum(tape.get(i,0) for i in range(lo,pos))
            out.append((step,left,tuple(runs)))
            if len(out)>=maxhomes: return out,None
        e=T[(st,v)]
        if e is None: return out,step
        tape[pos]=e[0];pos+=e[1];st=e[2]
        if pos>hi: hi=pos
        if pos<lo: lo=pos
    return out,None
def show(r): return " ".join("%d.%d"%(a,b) if i<len(r)-1 else "%d"%a for i,(a,b) in enumerate(r))
if __name__=="__main__":
    n=int(sys.argv[1]) if len(sys.argv)>1 else 3000000
    h,halt=homes(J,n)
    print(len(h),"home visits in",n,"steps")
    prev=None
    for step,left,r in h:
        key=tuple(r[1:])                       # print when anything behind the block changes
        if key!=prev: print("%9d  left:%d  %s"%(step,left,show(r)[:150]))
        prev=key
