#!/bin/bash
# batch3.sh LISTFILE TAG : for each wiring: every write-and-move choice (80 s at most) -> nest and growth test -> zone test.
# Keeps: z.WIRING = zone lines of every nested table,  and prints one line per wiring.
for w in $(cat $1); do timeout 80 ./flow $w 200000 2>/dev/null | cut -d' ' -f1 > a3.$2; n=$(wc -l < a3.$2); ./nestc 200000 < a3.$2 | cut -d' ' -f1 > b3.$2; ./zonec 4000000 < b3.$2 > z.$w; f=$(awk '$3>=7 && $3<=9 && $4>=1 && $4<=2 && $5==2 && $2>=1 && $7>=2.15' z.$w | wc -l); echo "$w alive $n nested $(wc -l < b3.$2) fit $f"; done
