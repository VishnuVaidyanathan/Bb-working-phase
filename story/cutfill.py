"""cutfill.py C E [pictures]   The BB(5) story with other numbers, played on the tape only (no table).
   cut: every C cells of the block keep one 1 (pieces 0..01);  fill: one sweep fills a piece and adds E on the left.
   BB(5) champion is C=3, E=2.  Prints the fate of the story, or the first PICTURES pass pictures as a story file."""
import sys
C=int(sys.argv[1]);E=int(sys.argv[2]);NP=int(sys.argv[3]) if len(sys.argv)>3 else 0
tape={};p=0;steps=0;pics=[];layers=0
def cfg(name):
    ks=[q for q in tape if tape[q]]+[p];lo,hi=min(ks),max(ks)
    return name+" "+"".join(("[%d]"%tape.get(q,0)) if q==p else str(tape.get(q,0)) for q in range(lo,hi+1))
def pic(name):
    global last
    pics.append((cfg(name),steps))
def left_pass():           # from W standing on a 1: walk left over the 1s, add E-1 cells, stop on the 0 as S
    global p,steps
    while tape.get(p,0)==1: p-=1;steps+=1
    for _ in range(E-1): tape[p]=1;p-=1;steps+=1
fate=None
pic("S")
while steps<10**9:
    # right pass from S on a 0
    tape[p]=1;p+=1;steps+=1
    while tape.get(p,0)==1: p+=1;steps+=1
    bad=False
    for _ in range(C-1):
        if tape.get(p,0)==1: bad=True
        tape[p]=1;p+=1;steps+=1
    if bad: fate="story breaks (a fill met a 1)";break
    if tape.get(p,0)==1:
        pic("W");left_pass()
        if tape.get(p,0)==1: fate="story breaks (left end not empty)";break
        pic("S");continue
    # the wall
    pic("W");tape[p]=1;p-=1;steps+=1;layers+=1;j=0
    while tape.get(p,0)==1:
        if j: tape[p]=0
        p-=1;steps+=1;j=(j+1)%C
    if j==0: pic("S");continue
    if j==C-1: fate="HALT in layer %d after %d steps, %d ones"%(layers,steps,sum(tape.values())+1);break
    pic("VXYZ"[j-1]);tape[p]=1;p+=1;steps+=1          # the middle roads: write a 1, turn, go left
    pic("W");left_pass();pic("S")
if NP:
    print("slack 3\nmargin 2")
    for (a,sa),(b,sb) in list(zip(pics,pics[1:]))[:NP]: print(a,"->",b,sb-sa)
else: print("C=%d E=%d :"%(C,E),fate or "no halt in 10^9 steps (%d layers)"%layers)
