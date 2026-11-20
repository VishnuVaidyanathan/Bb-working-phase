"""lay1.py K [parts] : our layout 1, written as loose pictures for free.c (no table is used to make them).
   Tape:   [0] 1^w 0 1^b 0 1^c ...      the head rests on the blank cell left of the block being built (w).
   Stores stand in a row to the right, each separated by one 0.  The nearest store (b) is the one being eaten.
   R  round      (w, b, ..)   -> (w+K, b-1, ..)    one cell eaten from b, one added at the right end of w, K-1 at the left end"""
import sys
K=int(sys.argv[1]);parts=sys.argv[2] if len(sys.argv)>2 else "R";L=44;PADL=12
def conf(w,stores,shift=0):
    # shift = how many cells left of the start position the block now begins ; gap = extra zeros eaten from the next store
    cells=[0]*L;head=PADL-shift;i=head+1
    for _ in range(w): cells[i]=1;i+=1
    return cells,head,i
def tape(w,stores,shift,eaten):
    cells,head,i=conf(w,stores,shift);i+=1+eaten        # the separating 0, then cells already eaten
    for k,s in enumerate(stores):
        for _ in range(s): cells[i]=1;i+=1
        i+=1
    return "".join(("[%d]"%x) if j==head else str(x) for j,x in enumerate(cells))
if "R" in parts:
    for w,b,c in [(1,1,0),(1,2,0),(2,1,0),(2,2,1),(3,1,2),(1,3,1),(2,3,0),(4,2,0)]:
        st=[b]+([c] if c else [])
        # before: w, then stores.  after: w grows by K (1 on the right over the old gap, K-1 on the left), b loses its first cell
        before=tape(w,st,0,0)
        cells=[0]*L;head=PADL-(K-1);i=head+1
        for _ in range(w+K): cells[i]=1;i+=1
        i+=1
        for s in [b-1]+st[1:]:
            for _ in range(s): cells[i]=1;i+=1
            i+=1
        after="".join(("[%d]"%x) if j==head else str(x) for j,x in enumerate(cells))
        print("S",before,"S",after,2,2*(w+K)+10)
