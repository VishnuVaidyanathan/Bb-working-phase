#!/bin/bash
cd /tmp/claude-0/-home-claude/4b1f9c95-7cd8-5462-90c3-009c8e8939ee/scratchpad/c7
f=p/$1.txt; grep -q DONE $f 2>/dev/null && exit 0
PRE=$1 ./roles7p 7 'BGCBD?EDFEAFCB' 1000 20000000 > $f.tmp 2> p/$1.err && mv $f.tmp $f
