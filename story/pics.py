"""pics.py TABLE FROM TO : the tape at every head turn, with repeats folded.  > = head about to go right, < = about to go left."""
import sys,re
tm=sys.argv[1];a=int(sys.argv[2]);b=int(sys.argv[3]);T={}
for s,x in enumerate(tm.split("_")):
    for k in (0,1):
        e=x[3*k:3*k+3];T[(s,k)]=None if e[2] in "Z-" else (int(e[0]),1 if e[1]=="R" else -1,ord(e[2])-65)
def fold(x):
    for w in ("1100","100","110","10","01","1","0"):
        x=re.sub(r'(?<![\d(])((?:%s){4,})'%w,lambda m:" %s^%d "%(("("+w+")") if len(w)>1 else w,len(m.group(0))//len(w)),x)
    return x
tape={};p=0;s=0;prev=None;laststep=None
for i in range(1,b+1):
    t=T[(s,tape.get(p,0))]
    if t is None: print("%8d  HALT in state %s"%(i,"ABCDEFG"[s]));break
    if i>=a and (prev is None or t[1]!=prev):
        ks=[q for q in tape if tape[q]]+[p];lo,hi=min(ks),max(ks)
        L="".join(str(tape.get(q,0)) for q in range(lo,p));R="".join(str(tape.get(q,0)) for q in range(p+1,hi+1))
        print("%8d  %s %s  %s [%d%s] %s"%(i,"ABCDEFG"[s],"->" if t[1]>0 else "<-",fold(L),tape.get(p,0),"",fold(R)))
    prev=t[1];tape[p]=t[0];p+=t[1];s=t[2]
