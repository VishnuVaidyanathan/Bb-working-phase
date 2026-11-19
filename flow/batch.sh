#!/bin/bash
# batch.sh LISTFILE : for each wiring, try all write-and-move choices (90 s at most), keep the tables that fit the recipe
for w in $(cat $1); do timeout 90 ./flow $w 200000 > f.$w 2>/dev/null; n=$(wc -l < f.$w); python3 recipe.py $w f.$w 0 > r.$w 2>/dev/null; echo "$w alive $n : $(head -1 r.$w)"; rm -f f.$w; done
