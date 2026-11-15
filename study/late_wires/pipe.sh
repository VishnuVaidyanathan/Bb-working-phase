#!/bin/bash
# usage: pipe.sh NAME   (reads NAME.txt with lines "seed table")
C=/tmp/claude-0/-home-claude/4b1f9c95-7cd8-5462-90c3-009c8e8939ee/scratchpad/c7
n=$1; cap=${2:-5000000}; qt=${3:-8}
awk '{print $2}' $n.txt | sort -u > $n.tabs
split -n l/2 $n.tabs $n.p.
($C/longrun $cap < $n.p.aa > $n.lr.aa & $C/longrun $cap < $n.p.ab > $n.lr.ab; wait)
cat $n.lr.a? > $n.lr; grep -v '^H' $n.lr | awk '{print $NF}' > $n.rx
split -n l/2 $n.rx $n.q.
($C/ncps 12 1000000 < $n.q.aa > $n.cps.aa & $C/ncps 12 1000000 < $n.q.ab > $n.cps.ab; wait)
cat $n.cps.a? | awk '$1=="U"{print $NF}' > $n.u
split -n l/2 $n.u $n.r.
(python3 qs3.py $n.r.aa $n.qs.aa $qt -r --exp-linear-rules --exp-meta-linear-rules --no-steps & python3 qs3.py $n.r.ab $n.qs.ab $qt -r --exp-linear-rules --exp-meta-linear-rules --no-steps; wait)
echo "$n: tables $(wc -l < $n.tabs), halt by plain run $(grep -c '^H' $n.lr), still running $(wc -l < $n.rx), not proved infinite $(wc -l < $n.u)"
cat $n.qs.a? | awk '{print $2}' | sort | uniq -c
