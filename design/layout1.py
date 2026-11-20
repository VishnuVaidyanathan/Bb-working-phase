"""layout1.py K F BITE [parts] [TURNS] : our layout 1, written as loose pictures for story/free (no table is used to make them).
   Tape:   [0] 1^w 0 1^b 0 1^c ...      the head rests on the blank cell left of the block being built (w).
   Stores stand in a row to the right, each separated by one 0.  The nearest store (b) is the one being eaten.
   R  round       (w, b, ..)     -> (w+K, b-1, ..)          one cell eaten from b, one added at the right end of w, K-1 at the left end
   P  promotion   (w, empty, c)  -> (F, w+1+BITE, c-BITE)   the block takes the empty store's place (it grows over the gap and the bitten cells),
                                                            the next store pays BITE, a fresh block of F starts on the left, one 0 away
   H  halt        (w, empty, c)  with c < BITE              -> HALT   (the leftover is the signal)"""
import sys
K=int(sys.argv[1]);F=int(sys.argv[2]);BITE=int(sys.argv[3]);parts=sys.argv[4] if len(sys.argv)>4 else "RPH";TURNS=int(sys.argv[5]) if len(sys.argv)>5 else 3;L=52;PADL=16
def tape(head,blocks):
    # blocks = list of (number of ones, zeros after); written from the cell right of the head
    cells=[0]*L;i=head+1
    for n,z in blocks:
        for _ in range(n): cells[i]=1;i+=1
        i+=z
    return "".join(("[%d]"%x) if j==head else str(x) for j,x in enumerate(cells))
if "R" in parts:
    for w,b,c in [(1,1,0),(1,2,0),(2,1,0),(2,2,1),(3,1,2),(1,3,1),(2,3,0),(4,2,0),(F,3,2),(F,4,0)]:
        rest=[(c,1)] if c else []
        print("S",tape(PADL,[(w,1),(b,1)]+rest),"S",tape(PADL-(K-1),[(w+K,1),(b-1,1)]+rest),2,2*(w+K)+10)
if "P" in parts:
    for w,c,d in [(2,BITE,0),(2,BITE+1,0),(3,BITE+2,0),(4,BITE,2),(5,BITE+1,1),(3,BITE+3,2),(6,BITE+2,0)]:
        rest=[(d,1)] if d else []
        print("S",tape(PADL,[(w,2),(c,1)]+rest),"S",tape(PADL-F-1,[(F,1),(w+1+BITE,1),(c-BITE,1)]+rest),TURNS,2*(w+F)+24)
if "H" in parts and BITE>1:
    for w,c,d in [(2,BITE-1,0),(3,BITE-1,2),(5,BITE-1,0)]:
        rest=[(d,1)] if d else []
        print("S",tape(PADL,[(w,2),(c,1)]+rest),"HALT",TURNS,2*w+24)
