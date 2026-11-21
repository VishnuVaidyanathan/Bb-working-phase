#!/bin/bash
# batch.sh LIST OUT : run the simulator 20 s on each table; one line each: table | rc | last useful line
: "${QUICK_SIM_DIR:?set QUICK_SIM_DIR to the Code folder of Shawn Ligocki's busy-beaver}"
while read t; do
  o=$(timeout 20 python3 $(dirname "$0")/../../calc/quick_sim_with_remainders.py "$t" --no-steps -r --exp-linear-rules --exp-meta-linear-rules 2>&1); rc=$?
  l=$(echo "$o" | grep -a -E "Num Nonzeros|Halt|Infinite|Error" | tail -2 | tr '\n' ' ' | cut -c1-260)
  echo "$t | rc=$rc | $l"
done < "$1" > "$2"
