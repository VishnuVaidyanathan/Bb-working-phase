import sys,resource,gc
sys.path.insert(0,"/home/claude/bb-working-phase/calc")
resource.setrlimit(resource.RLIMIT_AS,(2500*2**20,2500*2**20))
import learn2 as L
L.BIG=int(sys.argv[2])
for t in [l.strip() for l in open(sys.argv[1]) if l.strip()]:
    for b in [0]+list(range(3,25)):
        try: v=L.study(t,steps=1500000 if b==0 else 400000,first=b)
        except MemoryError: gc.collect();v="runs away (memory)"
        except Exception as e: v="ERROR "+str(e)[:60]
        print(t,"|","block %d"%b,"|",v,flush=True)
