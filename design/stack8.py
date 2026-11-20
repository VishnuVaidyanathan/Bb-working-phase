"""stack8.py : the 8-state stack machine as arithmetic (rules read off thought experiments, see README).
   block w, a row of stores.   round: (w, s) -> (w+3, s-1).
   store in front empty, g empty levels before a payer d:   if w+3 > 2g:  g fresh stores of 2 (the first is the new block), the old block becomes w+3-2g, the payer pays 1
                                                            if w+3 = 2k <= 2g: the block becomes k fresh stores exactly, nobody pays
                                                            if w+3 is odd and < 2g: HALT
   nothing behind:  w odd -> a new row of (w+3)/2 stores of 2 ;  w even -> HALT"""
import sys
def life(w,stores,maxev=10**6,cap=200000,trace=False):
    ev=0;rows=0;log=[]
    while ev<maxev:
        ev+=1
        while stores and stores[-1]==0: stores.pop()
        if not stores:
            if w%2==0: return "HALT",ev,rows,w,log
            n=(w+3)//2;rows+=1;log.append("new row of %s stores"%(n if n<10**9 else "about 2^%d"%n.bit_length()))
            if n>cap: return "row too long to follow",ev,rows,w,log
            w=2;stores=[2]*(n-1);continue
        if stores[0]>0:
            w+=3*stores[0];stores[0]=0
            if w.bit_length()>3000000: return "block too big to follow",ev,rows,w,log
            continue
        g=0
        while stores[g]==0: g+=1
        d=stores[g];rest=stores[g+1:];avail=w+3
        if avail>2*g: stores=[2]*(g-1)+[avail-2*g,d-1]+rest;w=2
        elif avail%2==0: k=avail//2;stores=[2]*(k-1)+[0]*(g-k)+[d]+rest;w=2
        else: return "HALT",ev,rows,w,log
    return "not finished",ev,rows,w,log
if __name__=="__main__":
    for b in range(1,40,2):
        r,ev,rows,w,log=life(b,[])
        print("first block %2d: %s after %d events, %d rows; %s; last block %s"%(b,r,ev,rows," -> ".join(log[:6]),w if w<10**12 else "about 2^%d"%w.bit_length()))
