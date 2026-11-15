"""Which wires do more than one job?
   A wire is one digit (state + symbol read).  Its job is read from what stands around it in the transcript:
   the digit before it and the digit after it.  Two different surroundings = two jobs.
   Runs (the same digit repeated) are counted once, so a filler walking a long block is one use.
   python3 jobs.py TABLE [steps]      or      python3 jobs.py --all machines.txt"""
import sys,collections,re
D="0123456789abcd"
def load(tm):
    c=tm.replace("1RZ","---").split('_');T={}
    for s in range(len(c)):
        for r in range(2):
            x=c[s][3*r:3*r+3];T[(s,r)]=None if x=='---' else (int(x[0]),1 if x[1]=='R' else -1,ord(x[2])-65)
    return T
def transcript(tm,N):
    T=load(tm);tape={};p=0;s=0;out=[];mv=[]
    for i in range(N):
        r=tape.get(p,0);t=T[(s,r)]
        if t is None: out.append(D[2*s+r]);mv.append(0);break
        out.append(D[2*s+r]);mv.append(t[1]);tape[p]=t[0];p+=t[1];s=t[2]
    return "".join(out),mv,T
def analyse(tm,N=1500000,minshare=0.0,mincount=3):
    d,mv,T=transcript(tm,N)
    # collapse runs of one digit, and runs of a repeated pair, to a single use
    toks=[];i=0
    while i<len(d):
        j=i
        while j<len(d) and d[j]==d[i]: j+=1
        toks.append((d[i],j-i));i=j
    seq=[t[0] for t in toks]
    ctx=collections.defaultdict(collections.Counter); uses=collections.Counter()
    for k in range(len(seq)):
        a=seq[k-1] if k>0 else "^"; b=seq[k+1] if k+1<len(seq) else "$"
        ctx[seq[k]][(a,b)]+=1; uses[seq[k]]+=1
    runlen=collections.defaultdict(list)
    for c,n in toks: runlen[c].append(n)
    res={}
    for w in sorted(ctx):
        tot=uses[w]
        jobs=[(a+w+b,c) for (a,b),c in ctx[w].most_common() if c>=mincount and c>=minshare*tot]
        mx=max(runlen[w]); filler=mx>=4
        k=D.index(w);t=T[(k//2,k%2)]
        res[w]=dict(jobs=jobs,uses=tot,filler=filler,maxrun=mx,act=(str(t[0])+("R" if t[1]>0 else "L")+"ABCDEFG"[t[2]]) if t else "halt")
    return res,len(d)
def line(tm,name=""):
    res,n=analyse(tm)
    multi=[w for w in res if len(res[w]['jobs'])>=2]
    tot=sum(max(1,len(res[w]['jobs'])) for w in res)
    return res,multi,tot
if __name__=="__main__":
    if sys.argv[1]=="--all":
        print("| id | wires | jobs in all | wires with 1 job | with 2 | with 3 or more | fillers | the wires with the most jobs |"); print("|---|---|---|---|---|---|---|---|")
        for l in open(sys.argv[2]):
            n,tm=l.split();res,multi,tot=line(tm)
            c=collections.Counter(min(3,max(1,len(res[w]['jobs']))) for w in res)
            top=sorted(res,key=lambda w:-len(res[w]['jobs']))[:3]
            print("| %s | %d | %d | %d | %d | %d | %s | %s |"%(n,len(res),tot,c[1],c[2],c[3],"".join(w for w in res if res[w]['filler']) or "-",", ".join("%s (%d)"%(w,len(res[w]['jobs'])) for w in top)))
    else:
        tm=sys.argv[1];res,multi,tot=line(tm)
        print(tm,"  wires",len(res)," jobs",tot)
        for w in res:
            r=res[w]
            print("  %s  %s  %-6s uses %-7d %s  jobs: %s"%(w,"ABCDEFG"[D.index(w)//2]+str(D.index(w)%2),r['act'],r['uses'],"filler(max run %d)"%r['maxrun'] if r['filler'] else "               ","   ".join("%s %s"%(j,("%d%%"%round(100*c/r["uses"])) if c>=0.01*r["uses"] else "x%d"%c) for j,c in r['jobs'])))
