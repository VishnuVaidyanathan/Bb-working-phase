"""wirings.py N SEED : N random wirings that obey the fixed part of the recipe:
   digit 0 flows to B (so the run starts 0 2), one halt (not on digit 0 or 2), every state is fed and reachable,
   and there are at least two loops to act as fillers (a digit flowing to its own state, or two states feeding each other)."""
import sys,random
N=int(sys.argv[1]);random.seed(int(sys.argv[2]));out=set()
while len(out)<N:
    w=[random.randrange(7) for _ in range(14)];w[0]=1
    h=random.choice([d for d in range(3,14)]);w[h]=-1
    fed=set(x for x in w if x>=0)
    if len(fed)<7: continue
    reach={0};ch=True
    while ch:
        ch=False
        for d in range(14):
            if d//2 in reach and w[d]>=0 and w[d] not in reach: reach.add(w[d]);ch=True
    if len(reach)<7: continue
    selfl=sum(1 for d in range(14) if w[d]==d//2)
    two=sum(1 for a in range(7) for b in range(a+1,7) if b in (w[2*a],w[2*a+1]) and a in (w[2*b],w[2*b+1]))
    if selfl+two<2 or selfl>4: continue
    out.add("".join("Z" if x<0 else "ABCDEFG"[x] for x in w))
print("\n".join(sorted(out)))
