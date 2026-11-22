"""bench.py : run a coordination GRAMMAR (not a machine) with exact whole numbers.  A paper tool; nothing proved.
   Grammar family (round +3, pay 2, land at the deepest empty level, fresh stores of 2, row end tested in twos):
     round   : front store f > 0                    -> block + 3f, front store 0
     payment : g empty levels, payer d >= 2         -> block B0, g-1 fresh stores of 2, then (block + AL - 2g), payer d-2
     payer 1 with a store of 2 or more behind it    -> HALT (base)
     payer 1, nothing behind (end of the row)       -> block odd: HALT (power);  even w: new row, R0 and w/2 + DL stores of 2, then a 1
   Free numbers: B0 (new block), AL (added to the landed block), R0 (block of a new row), DL (row length offset).
   Jeff Ketchersid's checked rule is B0=1 AL=7 (his new-row rule has a few more cases, see jeff/model.py).
   Usage: bench.py            - table of row chains for a grid of free numbers
          bench.py B0 AL R0 DL W0   - one chain, starting as if a row had just ended with the even block W0"""
import sys,time
BIG=3000000   # bits
def run_row(w,st,B0,AL,limit=400000,tmax=4.0):
    """work one row to its end.  returns ('end',w) , ('HALT base',info) , ('too big',info) """
    st=list(st);t0=time.time()
    for it in range(limit):
        if st and st[0]>0: w+=3*st[0];st[0]=0
        g=0
        while g<len(st) and st[g]==0: g+=1
        if g==len(st): return ("stuck",w)
        d=st[g];rest=st[g+1:]
        if d>=2:
            if g==1:
                n=d//2;p=3**n if n<BIG//2 else None
                if p is None: return ("too big","payer of %d bits"%d.bit_length())
                w=p*w+(B0+3*AL-6)*(p-1)//2;st[1]=d-2*n
            else:
                st=[2]*(g-1)+[w+AL-2*g,d-2]+rest;w=B0
            if w.bit_length()>BIG or time.time()-t0>tmax: return ("too big","block of %d bits, %d stores left"%(w.bit_length(),sum(1 for x in st if x)))
            continue
        if any(x>=2 for x in rest): return ("HALT base","payer 1 at level %d of %d"%(g+1,len(st)))
        return ("end",w)
    return ("too big","step limit")
def chain(B0,AL,R0,DL,W0,maxrows=6):
    out=[];w=W0
    for r in range(maxrows):
        if w%2: out.append("block %s odd: HALT (power)"%short(w));return out
        n=w//2+DL
        if n<1: out.append("row of %d: nothing"%n);return out
        if n>40: out.append("ROW OF %s STORES (not worked)"%short(n));return out
        res=run_row(R0,[2]*n+[1],B0,AL)
        if res[0]=="end": out.append("row %d -> block %s"%(n,short(res[1])));w=res[1]
        else: out.append("row %d: %s (%s)"%(n,res[0],res[1]));return out
    return out
def short(x):
    s=str(x) if x.bit_length()<200 else None
    return s if s else "[%d bits]"%x.bit_length()
if __name__=="__main__":
    if len(sys.argv)>5:
        print(" | ".join(chain(*map(int,sys.argv[1:6]))));sys.exit()
    for B0 in (0,1,2,3):
        for AL in range(1,10):
            for R0 in (2,3):
                for DL in (0,1):
                    for W0 in (2,4,6):
                        c=chain(B0,AL,R0,DL,W0)
                        print("B0=%d AL=%d R0=%d DL=%d start %d | %s"%(B0,AL,R0,DL,W0," | ".join(c)),flush=True)
