"""boots.py : route 1.  In Jeff Ketchersid's grammar (model.py rules), which small first rows end with a big EVEN block,
   i.e. are followed by a long second row?  Scan of first rows (block; stores ending in the end store 1)."""
import sys,itertools
sys.set_int_max_str_digits(0)
import model as M
def run(w,st,maxev=5000):
    """to the end of this row: ('HALT',block) | ('ROW',n_stores,block_before,new_block,new_stores) | ('?',...)"""
    for _ in range(maxev):
        st=list(st)
        if st and st[0]>0: w+=3*st[0];st[0]=0;continue
        r=M.step(w,st)
        if r is None: return ("?",w)
        if r=="HALT": return ("HALT",w)
        if len(r[1])>len(st)+2 or (len(r[1])>=3 and all(x in(2,3,4) for x in r[1][:-1]) and r[1][-1]==1 and r[0] in(2,3,4)): return ("ROW",len(r[1]),w,r[0],r[1])
        w,st=r[0],list(r[1])
        if w.bit_length()>100000: return ("BIG",w)
    return ("?",w)
if __name__=="__main__":
    from collections import Counter
    c=Counter();good=[]
    for L in (1,2,3,4):
        for body in itertools.product(range(0,7),repeat=L):
            if body[0]==0 and L>1 and all(x==0 for x in body): continue
            for w in range(1,9):
                st=list(body)+[1]
                o=run(w,st);c[o[0]]+=1
                if o[0]=="ROW" and o[1]>=23: good.append((sum(body)+w,w,st,o[1],o[2]))
    print("first rows tried:",sum(c.values()),dict(c))
    good.sort()
    def b(x): return str(x) if x<10**9 else "about 10^%d"%(len(str(x))-1)
    print("first rows followed by a row of 23 stores or more:",len(good))
    for s,w,st,n,blk in good[:40]: print("  block %d stores %s -> ends with block %s, next row %s stores"%(w,st,b(blk),b(n)))
