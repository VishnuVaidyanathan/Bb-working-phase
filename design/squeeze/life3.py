import sys,resource,gc
sys.path.insert(0,"/home/claude/bb-working-phase/calc")
resource.setrlimit(resource.RLIMIT_AS,(2500*2**20,2500*2**20))
import learn2 as L
L.BIG=4
for t in [l.strip() for l in open(sys.argv[1]) if l.strip()]:
    v="no row"
    for b in (27,28,29,0):
        try: v=L.study(t,steps=500000,first=b,life=True)
        except MemoryError: gc.collect();v="runs away (memory)"
        except Exception as e: v="ERROR "+str(e)[:60]
        if v.startswith("K="): break
    print(t,"|",v,flush=True)
