#!/bin/bash
# run_batch.sh : run search on the starts in starts84.txt that have no result yet, two at a time,
# starting no new one after 80 minutes.  Results: results/<start>.sum (counts) and results/<start>.rl (tables with a laying).
E=/tmp/claude-0/-home-claude/4b1f9c95-7cd8-5462-90c3-009c8e8939ee/scratchpad/eight
R=/home/claude/bb-working-phase/design/prefix
[ -x $E/search ] || { mkdir -p $E; gcc -O2 -o $E/search $R/search.c; }
t0=$(date +%s)
one(){ s="$1"; f=$(echo "$s" | tr -d ' '); $E/search "$s" 300 2> $E/$f.sum | awk -v o=$E/$f.rl '$1=="RL"{print > o} $1=="R"{r++} END{print "R-only tables:",r+0 > "/dev/stderr"}' 2> $E/$f.r; touch $E/$f.rl; cat $E/$f.r >> $E/$f.sum; cp $E/$f.rl $R/results/$f.rl; cp $E/$f.sum $R/results/$f.sum; }
while read s; do
  f=$(echo "$s" | tr -d ' '); [ -f $R/results/$f.sum ] && continue
  [ $(( $(date +%s) - t0 )) -gt 4800 ] && break
  while [ $(jobs -r | wc -l) -ge 2 ]; do sleep 5; done
  [ $(( $(date +%s) - t0 )) -gt 4800 ] && break
  one "$s" &
done < $R/starts84.txt
wait
echo "done: $(ls $R/results/*.sum 2>/dev/null | wc -l) of $(wc -l < $R/starts84.txt) starts"
