"""emerge.py FILE [BLOCKS] : what do tables that were only asked to play the round and the promotion do by themselves at deeper gaps?
   Each table is run on a hand tape (thought experiment); the stores at every promotion (rest with a fresh block) are its signature.
   Tables with the same signature are grouped."""
import sys,re
from collections import defaultdict
from play import play
blocks=[int(x) for x in sys.argv[2].split(',')] if len(sys.argv)>2 else [1,2,2,2,2]
groups=defaultdict(list)
for l in open(sys.argv[1]):
    if l[0] not in '01': continue
    tm=l.split()[0];m=re.search(r'S=(\w)',l);S=m.group(1) if m else 'A'
    if '---' in tm: tm2=tm
    o=play(tm,S,blocks,NS=400000,maxshow=100000)
    prom=[x for x in o if x.split()[0]=='1' or not x[0].isdigit()]
    end=o[-1] if not o[-1][0].isdigit() else ("still going, block %s"%o[-1].split()[0])
    sig=" | ".join(prom[1:9])+"  ..  "+end.split(" at step")[0]
    groups[sig].append(tm)
for sig,tms in sorted(groups.items(),key=lambda x:-len(x[1])):
    print("%3d tables, e.g. %s"%(len(tms),tms[0]));print("      "+sig[:230])
