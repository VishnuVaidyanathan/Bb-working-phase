"""layout2.py J HALTPARITY [parts] [TURNS] : our layout 2, as loose pictures for story/free (no table is used to make them).
   Tape:   [0] 1^w 0 1^b 0 1^c ...     as layout 1: the head rests left of the block, stores stand in a row to the right, one 0 apart.
   R  round            (w, b, ..)             -> (w+2, b-1, ..)
   P  promotion        (w, empty, c)          -> (1, w+2, c-1)       the block takes the empty store's place, the next store pays 1, a fresh block of 1 starts
   W  the same, deeper (w, empty, empty, d)   -> (1, w+3, d-1)       one rule for every depth: the next real store pays
   C  cut              (w, nothing at all)    -> the block, grown by J, is cut by 2 into stripes 10 10 10 ... : a block of 1 and stores of 1
   H  gate             the cut of a block whose grown size is odd (HALTPARITY=1) or even (HALTPARITY=0) is the halt"""
import sys
J=int(sys.argv[1]);HP=int(sys.argv[2]);parts=sys.argv[3] if len(sys.argv)>3 else "RPWCH";TURNS=int(sys.argv[4]) if len(sys.argv)>4 else 4;L=56;PADL=16
def tape(head,blocks):
    cells=[0]*L;i=head+1
    for n,z in blocks:
        for _ in range(n): cells[i]=1;i+=1
        i+=z
    return "".join(("[%d]"%x) if j==head else str(x) for j,x in enumerate(cells))
if "R" in parts:
    for w,b,c in [(1,1,0),(1,2,0),(2,1,0),(2,2,1),(3,1,2),(1,3,1),(2,3,0),(4,2,0),(1,4,0)]:
        rest=[(c,1)] if c else []
        print("S",tape(PADL,[(w,1),(b,1)]+rest),"S",tape(PADL-1,[(w+2,1),(b-1,1)]+rest),2,2*(w+2)+10)
if "P" in parts:
    for w,c,d in [(2,1,1),(2,2,0),(3,3,0),(4,1,2),(5,2,1),(3,4,2),(6,3,0)]:
        rest=[(d,1)] if d else []
        print("S",tape(PADL,[(w,2),(c,1)]+rest),"S",tape(PADL-2,[(1,1),(w+2,1),(c-1,1)]+rest),TURNS,2*w+26)
if "W" in parts:
    for w,d,e in [(2,1,1),(2,2,0),(3,3,0),(4,1,2),(5,2,1),(7,2,0)]:
        rest=[(e,1)] if e else []
        print("S",tape(PADL,[(w,3),(d,1)]+rest),"S",tape(PADL-2,[(1,1),(w+3,1),(d-1,1)]+rest),TURNS,2*w+30)
for w in [2,3,4,5,6,7,8,9]:
    g=w+J
    if g%2==HP:
        if "H" in parts: print("S",tape(PADL,[(w,6)]),"HALT",TURNS+2,4*w+40)
    elif "C" in parts:
        print("S",tape(PADL,[(w,6)]),"S",tape(PADL,[(1,1)]*(g//2)),TURNS+2,4*w+40)
