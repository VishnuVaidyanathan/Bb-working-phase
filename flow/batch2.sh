#!/bin/bash
# batch2.sh LISTFILE : for each wiring, try all write-and-move choices (90 s at most) and keep the tables whose filler has a nest (depth 3+) and whose tape grows
for w in $(cat $1); do timeout 90 ./flow $w 200000 2>/dev/null | cut -d' ' -f1 > a.$w; n=$(wc -l < a.$w); ./nestc 200000 < a.$w > n.$w; echo "$w alive $n nest $(wc -l < n.$w)"; rm -f a.$w; done
