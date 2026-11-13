# Cousin walk for BB(5).
# Start from the champion.  Change one wire at a time.  Keep a table if, from a blank tape, it HALTS and its
# grammar profile is in the same family (lines growing by a fixed amount, in runs whose lengths grow ~5/3).
# Tables are compared in normal form (states named in order of first use, first move to the right).
import sys, itertools, subprocess, collections
K=5
def parse(tm):
    T={}
    for s,part in enumerate(tm.split('_')):
        for b in (0,1):
            p=part[b*3:b*3+3]
            if p!='---' and p[2]!='Z': T[(s,b)]=(int(p[0]),1 if p[1]=='R' else -1,ord(p[2])-65)
    return T
def fmt(T):
    return '_'.join(''.join(('%d%s%s'%(T[(s,b)][0],'R' if T[(s,b)][1]>0 else 'L','ABCDE'[T[(s,b)][2]])) if (s,b) in T else '---' for b in (0,1)) for s in range(K))
def run(T,limit):
    """simulate from blank; returns (halted, steps, used wires in order of first use, line lengths)"""
    tape={}; pos=0; st=0; order=[]; seen=set(); lines=[]; last=0; lastd=1
    for t in range(limit):
        b=tape.get(pos,0); k=(st,b)
        if k not in seen: seen.add(k); order.append(k)
        if k not in T: return True,t,order,lines
        w,d,n=T[k]; tape[pos]=w; pos+=d; st=n
        if lastd==1 and d==-1: lines.append(t-last); last=t
        lastd=d
    return False,limit,order,lines
def normal(T):
    """rename states by first use from blank (short run), mirror so the first move is right, drop unused wires"""
    halted,steps,order,_=run(T,3000)
    used=[k for k in order if k in T]
    if not used: return None
    names={0:0}
    # order of first visit of states
    tape={}; pos=0; st=0
    for t in range(3000):
        k=(st,tape.get(pos,0))
        if k not in T: break
        w,d,n=T[k]
        if n not in names: names[n]=len(names)
        tape[pos]=w; pos+=d; st=n
    flip = T[(0,0)][1]==-1 if (0,0) in T else False
    N={}
    for (s,b),(w,d,n) in T.items():
        if s in names and n in names: N[(names[s],b)]=(w,-d if flip else d,names[n])
    return fmt(N)
def family(lines):
    """the grammar test: for lag 1 or 2, runs of equal line-length differences; take the runs with the largest
       positive difference; their lengths must grow by a ratio between 1.5 and 1.85, at least 6 times in a row"""
    for lag in (1,2):
        d=[lines[i]-lines[i-lag] for i in range(lag,len(lines))]
        runs=[(k,len(list(g))) for k,g in itertools.groupby(d)]
        pos=[k for k,n in runs if k>0 and n>=3]
        if not pos: continue
        top=collections.Counter(pos).most_common(1)[0][0]
        ls=[n for k,n in runs if k==top and n>=3]
        ok=0
        for a,b in zip(ls,ls[1:]):
            if a>=4 and 1.5<=b/a<=1.85: ok+=1
        if ok>=6: return top,ls
    return None
if __name__=='__main__':
    champ="1RB1LC_1RC1RB_1RD0LE_1LA1LD_1RZ0LA"
    known=[l.split() for l in open('known.txt')]
    vals=[(w,d,n) for w in (0,1) for d in (1,-1) for n in range(K)]
    start=normal(parse(champ)); seen={start:(0,None)}; frontier=[start]; fam={}
    LIM=int(sys.argv[1]); DEPTH=int(sys.argv[2])
    h,steps,_,lines=run(parse(start),LIM); fam[start]=(steps,family(lines))
    for depth in range(1,DEPTH+1):
        nxt=[]
        for tm in frontier:
            T=parse(tm)
            for s in range(K):
                for b in (0,1):
                    for v in vals+[None]:
                        U=dict(T)
                        if v is None: U.pop((s,b),None)
                        else: U[(s,b)]=v
                        if len(U)==2*K: continue                  # needs a halt wire
                        nm=normal(U)
                        if nm is None or nm in seen: continue
                        seen[nm]=(depth,tm)
                        halted,steps,_,lines=run(parse(nm),LIM)
                        if not halted or steps<100000: continue
                        f=family(lines)
                        if f is None: continue
                        fam[nm]=(steps,f); nxt.append(nm)
        print('depth',depth,': tables tried so far',len(seen),' cousins found so far',len(fam)); sys.stdout.flush()
        frontier=nxt
        if not frontier: break
    print()
    for tm,(steps,f) in sorted(fam.items(),key=lambda x:-x[1][0])[:40]:
        print('%9d  %s  depth %d  runs %s'%(steps,tm,seen[tm][0],f[1][-4:] if f else None))
    print('\nknown top-20 machines reached:')
    for rank,tm in known:
        nm=normal(parse(tm)); print('  #%s %s  %s'%(rank,tm,'REACHED at depth %d'%seen[nm][0] if nm in fam else ('seen but not kept' if nm in seen else 'not reached')))
