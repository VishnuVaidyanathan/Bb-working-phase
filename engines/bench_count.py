"""bench_count.py : the "count decides" grammar, run with exact numbers on the smallest cases (a paper tool; nothing proved).
   Same engine as bench.py (round +K, pay 2, land at the deepest empty level, fresh stores of 2), but the two meanings of
   "the payer has 1 left" are swapped:
       a store of 2 or more is behind it  ->  NEW ROW: the block w becomes w//2 stores of 2 and a 1, put in front of what is behind;
                                              the first real store behind pays 2
       nothing is behind it               ->  HALT
   Usage: bench_count.py K B0 AL R0  block store store ...      (K = cells added per round; K=3 is the real engine, K=1 a slow toy)"""
import sys,time
def run(K,B0,AL,R0,w,st,maxev=60,bits=200000,tmax=20):
    st=list(st);log=[];t0=time.time();rows=0;pays=0
    while True:
        if time.time()-t0>tmax or w.bit_length()>bits or len(st)>200000: log.append("TOO BIG to go on (block %d bits, %d stores)"%(w.bit_length(),len(st)));break
        if st and st[0]>0: w+=K*st[0];st[0]=0
        g=0
        while g<len(st) and st[g]==0: g+=1
        if g==len(st): log.append("stuck");break
        d=st[g];rest=st[g+1:]
        if d>=2:
            st=[2]*(g-1)+[w+AL-2*g,d-2]+rest;w=B0;pays+=1;continue
        j=next((i for i,x in enumerate(rest) if x>=2),None)
        if j is None:
            log.append("payer has 1 left and nothing behind: HALT   (rows made %d, payments %d, block %s)"%(rows,pays,w if w.bit_length()<60 else "[%d bits]"%w.bit_length()));break
        rows+=1;n=w//2
        behind=rest[:];behind[j]-=2
        if len(log)<maxev: log.append("row %d: block %s -> %s stores of 2 and a 1; behind it %s"%(rows,w if w.bit_length()<60 else "[%d bits]"%w.bit_length(),n if n.bit_length()<60 else "[%d bits]"%n.bit_length(),behind))
        st=[2]*n+[1]+behind;w=R0
    return log
if __name__=="__main__":
    a=list(map(int,sys.argv[1:]));print("\n".join(run(a[0],a[1],a[2],a[3],a[4],a[5:])))
