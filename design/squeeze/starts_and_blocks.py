import sys,resource,gc
sys.path.insert(0,"/home/claude/bb-working-phase/calc")
resource.setrlimit(resource.RLIMIT_AS,(2500*2**20,2500*2**20))
import learn2 as L
L.BIG=4
mode=sys.argv[1]
for t in [l.strip() for l in open(sys.argv[2]) if l.strip()]:
    its=[("start "+s,dict(start=s)) for s in "BCDEFGH"] if mode=="starts" else [("block %d"%b,dict(first=b)) for b in range(1,41)]
    for name,kw in its:
        try: v=L.study(t,steps=2000000,**kw)
        except MemoryError: gc.collect();v="runs away (memory)"
        except Exception as e: v="ERROR "+str(e)[:60]
        print(t,"|",name,"|",v,flush=True)
