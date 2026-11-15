"""Reading aid for any machine: digit counts, first appearances, the opening in blocks,
   and the tape at each use of the rarest wires.   python3 read.py TABLE STEPS [digits-to-watch]"""
import sys,re,collections
D="0123456789abcd"
def load(tm):
    c=tm.split('_');T={}
    for s in range(len(c)):
        for r in range(2):
            x=c[s][3*r:3*r+3];T[(s,r)]=None if (x=='---' or x[2] in 'ZH') else (int(x[0]),1 if x[1]=='R' else -1,ord(x[2])-65)
    return T
def rl(x,k=4):
    for mot in ("10","110","100","1100","1110","1000","101","1101","1011","011","001"):
        x=re.sub('(%s){3,}'%mot,lambda m:" (%s)^%d "%(mot,len(m.group(0))//len(mot)),x)
    return re.sub(r'([01])\1{%d,}'%(k-1),lambda m:f"{m.group(1)}^{len(m.group(0))} ",x)
def rd(x): return re.sub(r'(.)\1{3,}',lambda m:f"{m.group(1)}({len(m.group(0))})",x)
def tapestr(tape,p):
    ks=[k for k in tape if tape[k]]+[p];lo,hi=min(ks),max(ks)
    return rl("".join(str(tape.get(k,0)) for k in range(lo,p)))+" ["+str(tape.get(p,0))+"] "+rl("".join(str(tape.get(k,0)) for k in range(p+1,hi+1)))
if __name__=="__main__":
    tm=sys.argv[1];N=int(sys.argv[2]);watch=sys.argv[3] if len(sys.argv)>3 else None
    T=load(tm);tape={};p=0;s=0;cnt=collections.Counter();first={};dg=[];blocks=[];cur="";prev=0;start=1;ev=collections.defaultdict(list);halt=None
    for i in range(N):
        r=tape.get(p,0);d=D[2*s+r];t=T[(s,r)]
        if t is None: halt=i+1;dg.append(d);break
        w,m,q=t
        if cur and m>0 and prev<0:
            if len(blocks)<70: blocks.append((start,cur,t0))
            cur="";start=i+1
        if not cur: t0=tapestr(tape,p) if i<1500 else ""
        cnt[d]+=1;first.setdefault(d,i+1)
        if len(ev[d])<400: ev[d].append((i+1,tapestr(tape,p) if cnt[d]<=400 and len(tape)<6000 else ""))
        cur+=d;prev=m;dg.append(d);tape[p]=w;p+=m;s=q
    print(tm,"  steps run:",len(dg),"HALT at %d"%halt if halt else "")
    print("counts:"," ".join("%s:%d"%(d,cnt[d]) for d in sorted(cnt,key=lambda x:-cnt[x])))
    print("first seen:"," ".join("%s@%d"%(d,first[d]) for d in sorted(first,key=first.get)))
    print("opening blocks:")
    for st,c,t in blocks[:int(sys.argv[4]) if len(sys.argv)>4 else 40]: print("  %5d  %-30s %s"%(st,rd(c),t))
    rare=watch if watch else "".join(sorted(cnt,key=lambda x:cnt[x])[:2])
    for d in rare:
        print("tape at each use of digit",d,"(%d uses):"%cnt[d])
        for i,t in ev[d][:30]: print("  %9d  %s"%(i,t))
