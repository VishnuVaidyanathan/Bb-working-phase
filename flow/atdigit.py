"""atdigit.py TABLE DIGITS [STEPS [MAX]] : the tape every time one of the given digits is read (e.g. "6" or "ab"), folded.
   DIGITS may also be a road such as "2>8": then only when 8 is read straight after 2.
   Long rows of 1, of 10 and of 100 are written as 1^n, (10)^n, (100)^n.  The head is shown as [x] with the digit after it."""
import sys,re
tm=sys.argv[1];want=sys.argv[2];NS=int(sys.argv[3]) if len(sys.argv)>3 else 4000000;MAX=int(sys.argv[4]) if len(sys.argv)>4 else 40
H="0123456789abcd";T={}
for s,x in enumerate(tm.split("_")):
    for k in (0,1):
        e=x[3*k:3*k+3];T[(s,k)]=None if e[2] in "Z-" else (int(e[0]),1 if e[1]=="R" else -1,ord(e[2])-65)
def fold(x):
    for w in ("100","110","10","01","1"):
        x=re.sub(r'(?:%s){4,}'%w,lambda m:" %s^%d "%(("("+w+")") if len(w)>1 else w,len(m.group(0))//len(w)),x)
    return x
road=want.split('>') if '>' in want else None;prev='';tape=set();p=0;s=0;n=0
for i in range(1,NS+1):
    r=1 if p in tape else 0;d=H[2*s+r]
    if (d==road[1] and prev==road[0]) if road else (d in want):
        lo=min(min(tape),p) if tape else p;hi=max(max(tape),p) if tape else p
        L="".join("1" if q in tape else "0" for q in range(lo,p));R="".join("1" if q in tape else "0" for q in range(p+1,hi+1))
        print("%9d %s  %s [%d] %s"%(i,d,fold(L),r,fold(R)));n+=1
        if n>=MAX: break
    prev=d;t=T[(s,r)]
    if t is None: print("HALT at",i);break
    if t[0]: tape.add(p)
    else: tape.discard(p)
    p+=t[1];s=t[2]
