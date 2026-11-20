"""learn.py TABLE... | --list FILE : read a stack machine's rules off its own tape and follow it by arithmetic.
   Home visit = state A reading 0; the tape is then read as  block, store, store, ...
   1. In-row numbers: K (cells a round adds), m (size of a fresh store), read from the real run from a blank tape.
   2. End-of-row rule: the machine is started on a block of b cells with nothing behind, b = 12..59, and what it does is
      recorded (halt, or the new row).  The rule must repeat with b modulo 12 (else: no verdict).
   3. The real run gives the first big row (more than 8 stores).  The in-row arithmetic (stackcalc) is checked against the
      real run on that row, then gives the block W at the end of the row modulo 12, and the end rule gives the outcome.
   4. If it survives, the next row is tower-sized; the same is done for fresh rows of 1..14 stores to see what can happen.
   Verdicts are 'tested' only as far as these checks go - not proofs."""
import sys
sys.path.insert(0,__file__.rsplit('/',2)[0]+'/design')
import stackcalc as S,remainder as R
P=12
def parse(t):
    T={}
    for q,row in enumerate(t.split('_')):
        for b in (0,1):
            e=row[b*3:b*3+3];T[(chr(65+q),b)]=None if e[2] in 'Z-' else (int(e[0]),1 if e[1]=='R' else -1,e[2])
    return T
def homes(T,w,stores,maxsteps,maxhomes,start="A"):
    tape={};p=1
    for i in range(w): tape[p]=1;p+=1
    for s in stores:
        p+=1
        for i in range(s): tape[p]=1;p+=1
    pos=0;st=start;out=[];hi=p
    for step in range(maxsteps):
        v=tape.get(pos,0)
        if st=="A" and v==0:
            q=pos+1;w2=0
            while tape.get(q,0): w2+=1;q+=1
            ss=[];q+=1;z=0
            while q<=hi+2:
                c=0
                while tape.get(q,0): c+=1;q+=1
                ss.append(c);q+=1
            while ss and ss[-1]==0: ss.pop()
            out.append((w2,tuple(ss)))
            if len(out)>=maxhomes: return out
        e=T[(st,v)]
        if e is None: out.append("HALT");return out
        tape[pos]=e[0];pos+=e[1];st=e[2]
        if pos>hi: hi=pos
    return out
def inrow(K,m,w,stores):
    """one home visit of arithmetic inside a row; None if the row is used up or the block is too small"""
    stores=list(stores)
    if not stores: return None
    if stores[0]>0: stores[0]-=1;return (w+K,tuple(stores))
    g=0
    while g<len(stores) and stores[g]==0: g+=1
    if g==len(stores) or w+K<=m*g: return None
    return (m,tuple([m]*(g-1)+[w+K-m*g,stores[g]-1]+stores[g+1:]))
def study(tm,steps=6000000,start="A"):
    """start = the state the machine is started in on the blank tape (a free choice; rename states to make it A)"""
    T=parse(tm)
    if ("A",0) not in T or T[("A",0)] is None: return "no home state"
    real=homes(T,0,[],steps,10**7,start)
    if real and real[-1]=="HALT": return "halts small from a blank tape"
    big=[i for i,c in enumerate(real) if len(c[1])>8]
    if not big: return "no big row within %d steps"%steps
    i0=big[0];w0,st0=real[i0]
    # K and m from the row
    K=m=None
    for a,b in zip(real[i0:],real[i0+1:]):
        if b=="HALT": break
        if a[1] and b[1] and len(a[1])==len(b[1]) and a[1][0]-1==b[1][0] and a[1][1:]==b[1][1:]: K=b[0]-a[0];break
    from collections import Counter
    m=Counter(st0).most_common(1)[0][0]
    if not K or not m: return "numbers not read"
    # check the in-row arithmetic on the real run
    cur=(w0,st0);ok=0
    for c in real[i0+1:]:
        nxt=inrow(K,m,cur[0],cur[1])
        if nxt is None or c=="HALT" or tuple(x for x in nxt[1])!=c[1] or nxt[0]!=c[0]:
            if nxt is None: break
            return "in-row arithmetic differs from the real run (K=%d m=%d) after %d agreeing visits"%(K,m,ok)
        cur=c;ok+=1
    if ok<200: return "too few visits to check (K=%d m=%d, %d)"%(K,m,ok)
    # end-of-row rule by classes of b mod P
    rule={}
    for b in range(P,5*P):
        h=homes(T,b,[],400000,2)
        if len(h)<2: return "end rule not read (b=%d)"%b
        out=h[1]
        if out=="HALT": key=("HALT",)
        else:
            w1,s1=out;nm=0
            while nm<len(s1) and s1[nm]==m: nm+=1
            key=("ROW",w1,2*0+b-nm*(P and 1)*0,tuple(s1[nm:]),nm)     # nm = number of full stores
        rule.setdefault(b%P,[]).append((b,key))
    cls={}
    for r,lst in rule.items():
        kinds=set(k[0] for b,k in lst)
        if len(kinds)!=1: return "end rule does not repeat with b mod %d"%P
        if "HALT" in kinds: cls[r]=("HALT",);continue
        tails=set((k[1],k[3]) for b,k in lst)
        (b1,k1),(b2,k2)=lst[0],lst[1]
        slope=(k2[4]-k1[4],b2-b1)                     # full stores gained per P cells
        if len(tails)!=1 or any((k[4]-k1[4])*slope[1]!=(b-b1)*slope[0] for b,k in lst): return "end rule not regular"
        cls[r]=("ROW",k1[1],k1[3],b1,k1[4],slope)     # block, tail, at b1 has n1 full stores, slope
    D=S.Design(K,m)
    def outcome(Wnode):
        r=R.mod_(Wnode,P,{});return cls[r],r
    W=D.row_end(w0,list(st0))
    oc,r=outcome(W);n1=len(st0)
    head="K=%d m=%d, checked %d visits; first big row %d stores; "%(K,m,ok,n1)
    if oc[0]=="HALT": return head+"HALTS at the end of that row: about %d arrows"%(n1-2)
    # survives: what can fresh rows of this shape do?
    seen=[]
    shape=oc
    for depth in range(3):
        _,wb,tail,b1,nb1,slope=shape
        outs=[]
        for n in range(1,15):
            oc2,r2=outcome(D.row_end(wb,[m]*n+list(tail)));outs.append((oc2[0],r2))
        kinds=[o[0] for o in outs[4:]]
        if all(k=="HALT" for k in kinds): return head+"survives it; then HALTS at the end of the tower-sized row (every long row of that shape halts)"
        if all(k=="ROW" for k in kinds):
            rs=set(o[1] for o in outs[4:])
            if len(rs)==1:
                nxt=cls[list(rs)[0]]
                if (nxt[1],nxt[2])==(wb,tail): return head+"survives it; NEVER HALTS (every long row ends the same way and makes the same kind of row)"
                shape=nxt;continue
            return head+"survives it; long rows end in classes %s, all make new rows (never halts if this goes on)"%sorted(rs)
        return head+"survives it; at a tower-sized row the outcome depends on the row length: %s  <-- LOOK"%("".join("H" if k=="HALT" else "r" for k in [o[0] for o in outs]))
    return head+"survives it; no verdict"
if __name__=="__main__":
    a=sys.argv[1:]
    tabs=[l.split()[0] for l in open(a[1]) if l.strip()] if a and a[0]=="--list" else a
    for t in tabs:
        try: v=study(t)
        except Exception as e: v="ERROR "+str(e)[:80]
        print(t,"|",v,flush=True)
