"""rules6.py : thought experiments on the 6-state stack table found by letting tables arrange themselves (emerge.py).
   A tape is given as n.g,n.g,... (n ones then g zeros); the head rests left of it in state A.  Prints the tape at later rests."""
import sys,re
TM='1RB0LE_0RC0RB_1RA0LD_1LD1LA_1RC1LF_1LF1LE'
def go(spec,tm=TM,S='A',NS=3000000,maxrest=6,only_fresh=True):
    T={}
    for s,x in enumerate(tm.split("_")):
        for k in (0,1):
            e=x[3*k:3*k+3];T[(s,k)]=None if e[2] in "Z-" else (int(e[0]),1 if e[1]=="R" else -1,ord(e[2])-65)
    right='0'+''.join('1'*int(a)+'0'*int(b) for a,b in ((x.split('.')+['0'])[:2] for x in spec.split(',')))
    tape={i:int(c) for i,c in enumerate(right)};p=0;s=ord(S)-65;s0=s;out=[];lo=0;hi=len(right);last=None
    for i in range(NS):
        r=tape.get(p,0)
        if p<lo: lo=p
        if p>hi: hi=p
        if i>0 and s==s0 and r==0 and tape.get(p+1,0)==1 and not any(tape.get(q,0) for q in range(lo,p)):
            t="".join(str(tape.get(q,0)) for q in range(p+1,hi+1)).rstrip('0')
            d=" ".join("%d.%d"%(len(m.group(1)),len(m.group(2))) if m.group(2) else "%d"%len(m.group(1)) for m in re.finditer(r'(1+)(0*)',t))
            fresh=t.startswith('10')
            if d!=last and (fresh or not only_fresh): out.append(d);last=d
            if len(out)>=maxrest: break
        t=T[(s,r)]
        if t is None: out.append("STOPS at step %d (wire %s%d), ones %d"%(i,chr(65+s),r,sum(tape.values())));break
        tape[p]=t[0];p+=t[1];s=t[2]
        if p<-500000: out.append("runs away left");break
        if p>len(right)+500000: out.append("runs away right");break
    else: out.append("…")
    return out
if __name__=="__main__":
    for spec in sys.argv[1:]: print("%-22s -> %s"%(spec," | ".join(go(spec))[:200]))
