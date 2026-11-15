"""Jeff's machine started on a row of p pairs:  (10)^p [G reads 0].   Words and tapes."""
import re,collections,sys
tm="1RB0RG_1RC1RB_0RD1RZ_0LE0LD_0LF1LE_1RA1LF_1LC0RB".split('_');T={}
for s in range(7):
    for r in range(2):
        x=tm[s][3*r:3*r+3];T[(s,r)]=None if x[2]=='Z' else (int(x[0]),1 if x[1]=='R' else -1,ord(x[2])-65)
D="0123456789abcd"
def rl(x):
    x=re.sub(r'(10){3,}',lambda m:f"(10)^{len(m.group(0))//2} ",x)
    x=re.sub(r'(1100){2,}',lambda m:f"(1100)^{len(m.group(0))//4} ",x)
    return re.sub(r'([01])\1{3,}',lambda m:f"{m.group(1)}({len(m.group(0))})",x)
def words(d):
    out=[];i=0
    pats=[(r'a1d(3*)2468(b+)',lambda m:"Count(%d)"%len(m.group(1)) if len(m.group(2))==len(m.group(1))+1 else "a1d 3(%d) Close(%d)"%(len(m.group(1)),len(m.group(2)))),
          (r'2476(9*)8a0(3*)',lambda m:"Round(%d)"%len(m.group(1)) if len(m.group(1))==len(m.group(2)) else "2476 9(%d) 8a0 3(%d)"%(len(m.group(1)),len(m.group(2)))),
          (r'2468(b+)',lambda m:"Close(%d)"%len(m.group(1))),
          (r'a1c476(9*)8b',lambda m:"Carry(%d)"%len(m.group(1))),
          (r'a1c476(9*)8a0(3+)',lambda m:"CarryOpen(%d,%d)"%(len(m.group(1)),len(m.group(2)))),
          (r'c476(9*)8a0(3+)',lambda m:"Open(%d,%d)"%(len(m.group(1)),len(m.group(2)))),
          (r'c476(9*)8ba1',lambda m:"Wait(%d)"%len(m.group(1))),
          (r'a1d(3*)(?=2476)',lambda m:"a1d 3(%d)"%len(m.group(1))),
          (r'2476(9+)8ba1',lambda m:"Walk(%d)"%len(m.group(1)))]
    while i<len(d):
        for p,f in pats:
            m=re.compile(p).match(d,i)
            if m: out.append(f(m));i=m.end();break
        else:
            if out and out[-1].startswith("'"): out[-1]=out[-1][:-1]+d[i]+"'"
            else: out.append("'"+d[i]+"'")
            i+=1
    return out
def run(p,cap):
    tape=collections.defaultdict(int)
    for i in range(p): tape[-2*i-2]=1
    pos=0;s=6;dg=[];ev=[];res="not finished in %d steps"%cap
    for i in range(cap):
        r=tape[pos]
        if s==6 and r==0:
            ks=[k for k in tape if tape[k]]
            if ks:
                lo,hi=min(ks),max(ks)
                L="".join(str(tape[k]) for k in range(lo,pos));R="".join(str(tape[k]) for k in range(pos+1,hi+1))
                ev.append((i,rl(L)+" [G0] "+rl(R),L,R))
                if i>0 and R=="" and re.fullmatch(r'(10)+',L): res="PAIRS %d at step %d"%(len(L)//2,i);break
        t=T[(s,r)]
        if t is None: res="HALT at step %d, %d ones"%(i+1,sum(tape.values()));dg.append(D[2*s+r]);break
        dg.append(D[2*s+r]);tape[pos]=t[0];pos+=t[1];s=t[2]
    return "".join(dg),ev,res
if __name__=="__main__":
    for p in [int(x) for x in sys.argv[1:]]:
        d,ev,res=run(p,400000)
        print("=== %d pairs  ->  %s"%(p,res))
        print("   words:"," ".join(words(d[:700])))
        for i,t,L,R in ev[:14]: print("   %6d  %s"%(i,t))
