"""pushers.py [STEPS] : the digits that do not grow.  For each machine: the run digits (digits that follow themselves) and the
   words made of all the other digits between two runs - which run comes before, the word, which run comes after, and how often.
   A word is a turn (run x -> word -> run y).  This is the "arrangement" of the pushing digits."""
import sys
from collections import Counter
H="0123456789abcdef"
def digits(tm,n,state=0,tape=None,pos=0):
    T=[[None if e[2] in "Z-" else (int(e[0]),1 if e[1]=="R" else -1,ord(e[2])-65) for e in (r[:3],r[3:])] for r in tm.split("_")]
    tp=dict(tape or {});s=state;p=pos;out=[]
    for _ in range(n):
        b=tp.get(p,0);out.append(H[2*s+b]);e=T[s][b]
        if e is None: break
        tp[p]=e[0];p+=e[1];s=e[2]
    return "".join(out)
def report(name,tm,n,**kw):
    d=digits(tm,n,**kw)
    runs=sorted(set(a for a,b in zip(d,d[1:]) if a==b))
    c=Counter(d);words=Counter();i=0;L=len(d)
    while i<L:
        if d[i] in runs: i+=1;continue
        j=i
        while j<L and d[j] not in runs: j+=1
        words[(d[i-1] if i else "^",d[i:j],d[j] if j<L else "$")]+=1;i=j
    used=[x for x in H if x in c]
    print("\n%s  %s"%(name,tm))
    print("  digits used %d; run digits: %s ; share of all digits in runs: %.2f%%"%(len(used),", ".join("%s (%d)"%(r,c[r]) for r in runs),100*sum(c[r] for r in runs)/L))
    print("  pushing digits: %d ; different words: %d"%(len(used)-len(runs),len(words)))
    for (a,w,b),k in words.most_common(14): print("     %s| %-12s |%s   %8d times   (%d digits)"%(a,w,b,k,len(w)))
if __name__=="__main__":
    n=int(sys.argv[1]) if len(sys.argv)>1 else 2000000
    report("Jeff Ketchersid, BB7 champion","1RB0RG_1RC1RB_0RD1RZ_0LE0LD_0LF1LE_1RA1LF_1LC0RB",n)
    report("Pavel Kropitz, earlier BB7 champion","1RB0RA_1LC1LF_1RD0LB_1RA1LE_1RZ0LC_1RG1LD_0RG0RF",n)
    report("Marxen and Buntrock, BB5 champion","1RB1LC_1RC1RB_1RD0LE_1LA1LD_1RZ0LA",n)
    report("our tower halter","1RB0LC_1RD1RE_1LF1LA_1RC1LF_1LF1RZ_1RG1LD_0RA1RG",n)
    report("our 8-state stack, first block 5 (hand tape)","1LH1RG_1RC1RB_0LF0LD_0LF1LD_0LD0RB_0RA1LF_1RZ1RE_1RB---",n,tape={i:1 for i in range(1,6)})
