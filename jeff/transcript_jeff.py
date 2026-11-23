"""transcript_jeff.py : Jeff Ketchersid's champion written as a transcript in Vishnu's digits
   (A0=0 A1=1 B0=2 B1=3 C0=4 C1=5 D0=6 D1=7 E0=8 E1=9 F0=a F1=b G0=c G1=d), repeats folded as 3x7.
   Real run from a blank tape.  Part 1: the start, cut at each home visit.  Part 2: one example of each kind of event
   (round, payment with 1 empty level, payment with 2, new row), named by our checked rules (model.py).
   Thought tool; credit for the machine: Jeff Ketchersid."""
import homes as H,model as M
T=H.parse(H.J);D="0123456789abcd"
tape={};pos=0;st="A";hi=0;lo=0;seq=[];prev=None;seen={};n=0
def fold(s):
    o=[]
    for d in s:
        if o and o[-1][0]==d: o[-1][1]+=1
        else: o.append([d,1])
    return " ".join(d if k==1 else "%sx%d"%(d,k) for d,k in o)
def read():
    runs=[];q=pos+1
    while q<=hi+1:
        a=0
        while tape.get(q,0): a+=1;q+=1
        b=0
        while q<=hi+1 and not tape.get(q,0): b+=1;q+=1
        runs.append((a,b))
    if runs and runs[-1][0]==0: runs.pop()
    return M.dec(runs),sum(tape.get(i,0) for i in range(lo,pos))
def short(c): return ("(%d; %s)"%(c[0]," ".join(map(str,c[1]))))[:60]
print("PART 1: the start from a blank tape")
for s in range(3000000):
    v=tape.get(pos,0)
    if st=="A" and v==0:
        c,left=read()
        if left==1 or prev is None:
            if prev is not None:
                stz=list(prev[1])
                if stz and stz[0]>0: kind="round"
                else:
                    g=0
                    while g<len(stz) and stz[g]==0: g+=1
                    kind="start / lone block" if g==len(stz) else ("payment, %d empty level%s"%(g,"s" if g>1 else "") if stz[g]>=2 else "new row")
                n+=1
                if n<=9: print("  %-28s %s -> %s\n      %s"%(kind,short(prev),short(c),fold(seq)[:230]))
                if kind not in seen or (len(seq)<len(seen[kind][0]) and kind!="round"): seen[kind]=(seq,prev,c)
            prev=c;seq=[]
    e=T[(st,v)]
    if e is None: break
    seq.append(D["ABCDEFG".index(st)*2+v]);tape[pos]=e[0];pos+=e[1];st=e[2];hi=max(hi,pos);lo=min(lo,pos)
print("\nPART 2: the shortest example of each kind seen in 3,000,000 steps")
for k,(q,a,b) in seen.items():
    print("  %s:  %s -> %s\n      %s"%(k,short(a),short(b),fold(q)[:420]))
