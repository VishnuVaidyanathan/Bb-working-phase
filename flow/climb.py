"""climb.py SEEDFILE MINUTES [BEAM] : climb toward a table that passes every line of the scorecard.
   Start from the seed tables.  Each round: take the best tables so far (the beam), change one wire of each in every
   possible way, throw out tables whose halt cannot be hit, keep those whose filler is nested and whose tape grows,
   score them on all 15 lines, and go again from the new best.  Everything scored is appended to climb.log
   (table, score, the 15 marks).  Stops after MINUTES."""
import sys,time,subprocess,os,random
from haltalive import check
from neighbours import single
from scorecard import score
D=os.path.dirname(os.path.abspath(__file__))
seeds=[l.split()[0] for l in open(sys.argv[1]) if l.strip()];T0=time.time();LIM=float(sys.argv[2])*60;BEAM=int(sys.argv[3]) if len(sys.argv)>3 else 60
seen=set();scored={}
if os.path.exists("climb.log"):
    for l in open("climb.log"):
        f=l.split()
        if len(f)>=4: scored[f[0]]=(int(f[1]),f[2],float(f[3]));seen.add(f[0])
log=open("climb.log","a")
def nested(tabs):
    r=subprocess.run([os.path.join(D,"nestc"),"200000","3","100"],input="\n".join(tabs)+"\n",capture_output=True,text=True).stdout
    return [l.split()[0] for l in r.splitlines() if l.strip()]
def do_score(tabs):
    tabs=[t for t in tabs if t not in scored]
    for i in range(0,len(tabs),400):
        res=score(tabs[i:i+400])
        for t,(sc,p,info) in res.items():
            m="".join("Y" if x else "." for x in p);scored[t]=(sc,m,info["growth"]);log.write("%s %d %s %.2f\n"%(t,sc,m,info["growth"]));log.flush()
do_score(seeds);expanded=set();rnd=0
while time.time()-T0<LIM:
    rnd+=1
    cand=sorted((t for t in scored if t not in expanded),key=lambda t:(-scored[t][0],-min(scored[t][2],2.6)+random.random()*0.02))[:BEAM]
    if not cand: break
    new=set()
    for t in cand:
        expanded.add(t)
        for n in single(t):
            if n not in seen: seen.add(n);new.add(n)
    alive=[t for t in new if check(t)[0]=="alive"]
    keep=nested(alive) if alive else []
    do_score(keep)
    best=max(v[0] for v in scored.values());hist={}
    for v in scored.values(): hist[v[0]]=hist.get(v[0],0)+1
    print("round %d  %.0f min  tried %d  alive %d  nested %d  scored so far %d  best %d  (15:%d 14:%d 13:%d 12:%d)"%(rnd,(time.time()-T0)/60,len(new),len(alive),len(keep),len(scored),best,hist.get(15,0),hist.get(14,0),hist.get(13,0),hist.get(12,0)),flush=True)
