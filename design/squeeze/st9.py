import sys,resource,gc
sys.path.insert(0,"/home/claude/bb-working-phase/calc")
resource.setrlimit(resource.RLIMIT_AS,(2500*2**20,2500*2**20))
import learn2 as L
L.BIG=4
for t in [l.strip() for l in open(sys.argv[1]) if l.strip()]:
    for s in "ABCDEFGHI":
        try: v=L.study(t,steps=2000000,start=s)
        except MemoryError: gc.collect();v="runs away (memory)"
        except Exception as e: v="ERROR "+str(e)[:60]
        print(t,"|","start "+s,"|",v,flush=True)
