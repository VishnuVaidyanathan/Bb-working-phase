"""digits.py TABLE [SHOW [STEPS]] : a table shown in digits.
   The first SHOW digits from a blank tape with repeats folded as x(n), then every digit with what comes before and after it
   (counted over STEPS steps), then the filler and the tops of its nest."""
import sys,re
from collections import Counter
sys.path.insert(0,__file__.rsplit("/",1)[0])
from nest import transcript,runs,depth
H="0123456789abcd"
def fold(S):
    out=[];i=0
    while i<len(S):
        best=None
        for L in range(1,9):
            w=S[i:i+L];n=1
            while S[i+n*L:i+(n+1)*L]==w: n+=1
            if n>=(3 if L<=2 else 2) and (best is None or n*L>best[0]*best[1]): best=(n,L)
        if best: n,L=best;w=S[i:i+L];out.append((w if L==1 else "("+w+")")+"(%d)"%n);i+=n*L
        else: out.append(S[i]);i+=1
    return "".join(out)
if __name__=="__main__":
    tm=sys.argv[1];show=int(sys.argv[2]) if len(sys.argv)>2 else 400;NS=int(sys.argv[3]) if len(sys.argv)>3 else 1000000
    S=transcript(tm,NS);c=Counter(zip(S,S[1:]))
    print(tm);print("first %d digits: %s"%(show,fold(S[:show])))
    for i,x in enumerate(tm.split("_")):
        for k in (0,1):
            d=H[2*i+k];e=x[3*k:3*k+3]
            act="HALT" if e[2]=="Z" else ("not used yet" if e[2]=="-" else "write %s, %s, %s"%(e[0],"right" if e[1]=="R" else "left",e[2]))
            bef=", ".join("%s (%s)"%(a,format(n,",")) for (a,b),n in sorted(c.items()) if b==d) or "never"
            aft=", ".join("%s (%s)"%(b,format(n,",")) for (a,b),n in sorted(c.items()) if a==d) or "-"
            print("  %s  %-18s | after: %-40s | goes to: %s"%(d,act,bef,aft))
    loop,r=runs(S);r=[x for x in r if x>=2];dd,trail=depth(r)
    print("filler %s, %d runs, nest depth %d"%(loop,len(r),dd));print("  run lengths:",r[:36])
    for i,t in enumerate(trail): print("  tops, level %d:"%(i+1),t[:16])
