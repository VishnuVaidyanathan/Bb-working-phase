"""arrangements.py [LIST [STEPS]] : how each machine arranges its digits.
   Growing digits = digits that follow themselves (a walk).  Per state: W = walker (one digit grows, the other turns),
   B = brancher (both digits push), G = the state holding the halt (with what its other digit does), 1 = only one digit ever used.
   Words = strings of pushing digits between two walks."""
import sys,re
from collections import Counter
sys.path.insert(0,__file__.rsplit('/',2)[0]+'/flow')
from pushers import digits,H
def study(tm,n):
    d=digits(tm,n);c=Counter(d);L=len(d);ns=tm.count("_")+1
    runs=set(a for a,b in zip(d,d[1:]) if a==b)
    words=Counter();inword={};i=0
    while i<L:
        if d[i] in runs: i+=1;continue
        j=i
        while j<L and d[j] not in runs: j+=1
        w=d[i:j];words[w]+=1
        for x in set(w): inword.setdefault(x,set()).add(w)
        i=j
    rows=tm.split("_");roles=[]
    for s in range(ns):
        a,b=H[2*s],H[2*s+1];halt=[x for x,e in ((a,rows[s][:3]),(b,rows[s][3:])) if e[2] in "Z-"]
        used=[x for x in (a,b) if x in c]
        if halt: roles.append("G" if len(used)>=1 else "g")
        elif any(x in runs for x in used): roles.append("W")
        elif len(used)==2: roles.append("B")
        else: roles.append("1")
    share=100*sum(c[r] for r in runs)/L
    top=sum(k for w,k in words.most_common(2))/max(1,sum(words.values()))*100
    return dict(roles="".join(roles),nruns=len(runs),share=share,nwords=len(words),top2=top,push=len(c)-len(runs),halted=(L<n))
if __name__=="__main__":
    lst=sys.argv[1] if len(sys.argv)>1 else __file__.rsplit('/',1)[0]+"/bb7_machines_from_wiki.txt"
    n=int(sys.argv[2]) if len(sys.argv)>2 else 2000000
    print("%-52s %-28s %-8s %5s %7s %6s %6s  %s"%("table","size","states","walks","walk %","words","top2 %","W B G 1"))
    for line in open(lst):
        if line.startswith("#") or not line.strip(): continue
        p=[x.strip() for x in line.split("|")];tm=p[0]
        if not re.fullmatch(r"([01][LR][A-Z]|---){2}(_([01][LR][A-Z]|---){2})*",tm): print(tm,"NOT A VALID TABLE");continue
        r=study(tm,n);ro=r["roles"]
        print("%-52s %-28s %-8s %5d %6.1f%% %6d %5.0f%%  %d %d %d %d%s"%(tm,p[1][:28] if len(p)>1 else "",ro,r["nruns"],r["share"],r["nwords"],r["top2"],ro.count("W"),ro.count("B"),ro.count("G")+ro.count("g"),ro.count("1")," (halted early?)" if r["halted"] else ""))
