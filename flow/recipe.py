"""recipe.py WIRING file.flow : keep the tables whose run fits the recipe written in digits:
   1. a word of three digits that always stick together (like 479 in Pavel's, 159 in BB(5))
   2. about 9 digits that branch (go to two digits)
   3. at least 9 roads used about equally often (the river)
   4. fillers (loops) that are used far more than the river, and more so later in the run (they grow with depth)"""
import sys
wir=sys.argv[1];H="0123456789abcd";nx=[None if c=="Z" else ord(c)-65 for c in wir]
def roads(v,off):
    r={}
    for a in range(14):
        if nx[a] is None: continue
        for k in (0,1):
            c=v[4*a+off+k]
            if c: r[(a,2*nx[a]+k)]=c
    return r
out=[]
for line in open(sys.argv[2]):
    f=line.split();tm=f[0];v=list(map(int,f[2:]))
    R=roads(v,0);Q=roads(v,2)
    outs={a:[b for (x,b) in R if x==a] for a in range(14)}
    branch=[a for a in outs if len(outs[a])==2]
    # fillers: loops (a->a, or a->b->a) 
    loops={k:c for k,c in R.items() if k[0]==k[1] or ((k[1],k[0]) in R and R[(k[1],k[0])]>0.5*c and c>0.5*R[(k[1],k[0])])}
    rest=sorted(c for k,c in R.items() if k not in loops)
    # river: biggest group of roads with counts within 6 percent
    best=(0,0,0)
    for i in range(len(rest)):
        j=i
        while j+1<len(rest) and rest[j+1]<=rest[i]*1.20: j+=1
        if j-i+1>best[0] and rest[i]>=20: best=(j-i+1,rest[i],rest[j])
    nriver,rlo,rhi=best
    if nriver<7 or not loops: continue
    fill=max(loops.values())
    if fill<10*rhi: continue
    # growth: filler per river round, now and at a quarter of the run
    qriv=sorted(c for k,c in Q.items() if k in R and rlo<=R[k]<=rhi)
    if not qriv or qriv[len(qriv)//2]==0: continue
    qfill=max(Q.get(k,0) for k in loops)
    g=(fill/rhi)/(max(qfill,1)/qriv[len(qriv)//2])
    if g<2.15: continue
    # sticking triple a->b->c inside the river
    tri=[]
    for (a,b),c in R.items():
        if a==b or not (rlo<=c<=rhi): continue
        if c<0.85*sum(R.get((a,x),0) for x in range(14)): continue
        for (b2,c2),cc in R.items():
            if b2==b and c2!=b and cc>=0.85*sum(R.get((b,x),0) for x in range(14)) and rlo*0.9<=cc<=rhi*1.1: tri.append(H[a]+H[b]+H[c2])
    if not tri or not (7<=len(branch)<=11): continue
    out.append((tm,len(branch),nriver,rlo,fill,round(g,2),",".join(sorted(set(tri))[:4])))
print("%d of %d tables fit the recipe"%(len(out),sum(1 for _ in open(sys.argv[2]))))
for o in sorted(out,key=lambda x:-x[5])[:int(sys.argv[3]) if len(sys.argv)>3 else 12]: print("  %s  branches %d  river roads %d (about %d each)  filler %d  growth %.2f  sticks %s"%o)
open(sys.argv[2]+".fit","w").write("\n".join(o[0] for o in out)+"\n")
