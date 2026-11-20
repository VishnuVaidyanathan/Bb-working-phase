"""stackgen.py : the stack design as arithmetic with its numbers left open, to choose them BEFORE building a table.
   K = cells a round adds;  m = size of a fresh store (a mark);  one look past an empty level costs the block m cells (net);
   when the block runs out with r cells left (0 < r < m): if r == RH the machine halts, otherwise the r cells stay as a short store.
   From a blank tape (block 0, nothing behind) follow the rows until a halt or until the numbers are too big to count."""
import sys
def life(K,m,RH,maxev=400000,cap=3000):
    w=0;stores=[];rows=[];ev=0
    def runout(avail,g_empties,rest):
        # the block (avail cells) is cut into marks of m; returns new (w, stores) or None for halt
        k,r=divmod(avail,m)
        marks=[m]*k
        if r:
            if r==RH: return None
            marks=marks+[r]              # the short leftover is the last (rightmost) mark
        if not marks: return (0,[0]*g_empties+rest)   # cannot happen: avail>0
        return (marks[0],marks[1:]+[0]*max(0,g_empties-len(marks))+rest)
    while ev<maxev:
        ev+=1
        while stores and stores[-1]==0: stores.pop()
        if not stores:
            avail=w+K;res=runout(avail,0,[])
            if res is None: return "HALT",rows,w
            w,stores=res;rows.append(len(stores)+1)
            if len(stores)>cap: return "climbing (row too long to count)",rows,w
            continue
        if stores[0]>0:
            w+=K*stores[0];stores[0]=0
            if w.bit_length()>200000: return "climbing (block too big to count)",rows,w
            continue
        g=0
        while stores[g]==0: g+=1
        d=stores[g];rest=stores[g+1:];avail=w+K
        if avail>m*g: w,stores=m,[m]*(g-1)+[avail-m*g,d-1]+rest
        else:
            res=runout(avail,g,[d]+rest)
            if res is None: return "HALT",rows,w
            w,stores=res
    return "climbing (too many events to count)",rows,w
if __name__=="__main__":
    for K in (2,3,4,5):
        for m in (2,3,4):
            for RH in range(1,m):
                r,rows,w=life(K,m,RH)
                print("round +%d, fresh store %d, halt on %d left over: %-38s rows %s, last block %s"%(K,m,RH,r,rows[:10],w if w<10**9 else "about 2^%d"%w.bit_length()))
