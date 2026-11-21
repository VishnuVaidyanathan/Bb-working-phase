"""rows3.py : towers over towers by arithmetic.  For each stack design (round +K, fresh store m, halt on leftover RH), from a blank tape:
   follow the small rows exactly, then the first big row by its formula, then the tower-long rows after it by the settled leftover rule
   of rows2.py (leftover after a long cut row whose last store is r; taken from rows of 6 and 7 stores, which must agree).
   Prints the designs that HALT, with the number of tower-long rows worked before the halt.  Arithmetic only; no machine is built here."""
import sys,signal
import stackcalc as S
import remainder as R
class TO(Exception): pass
def alarm(*a): raise TO()
signal.signal(signal.SIGALRM,alarm)
def settled(K,m):
    D=S.Design(K,m);f={}
    for r in range(m):
        v=[]
        for n in (6,7):
            try:
                signal.alarm(30);v.append((R.mod_(D.row_end(m,[m]*(n-1)+([r] if r else [])),m,{})+K)%m);signal.alarm(0)
            except TO: v.append(None)
        f[r]=v[0] if v[0]==v[1] else ("alt",v[0],v[1])
    return f
def follow(K,m,RH,f,maxrows=12):
    D=S.Design(K,m);rows=[];w=0;stores=[]
    for _ in range(maxrows):
        res=S.plain(K,m,RH,w,stores,bits=20000,maxev=200000) if len(stores)<=40 else ("BIG",None)
        if res[0]=="HALT": return ("halt inside a small row",rows,0)
        if res[0]=="ROW":
            marks=S.cut(res[1]+K,m,RH)
            if marks is None: return ("halt at a row end",rows,0)
            rows.append(len(marks)-1);w=marks[0];stores=marks[1:];continue
        try:
            signal.alarm(60);r=(R.mod_(D.row_end(w,stores),m,{})+K)%m;signal.alarm(0)
        except TO: return ("too slow",rows,0)
        if r==RH: return ("halt at the end of the first big row",rows,0)
        extra=0;seen=set()
        while True:                      # tower-long rows: last store r
            if r in seen: return ("never halts (leftovers cycle)",rows,extra)
            seen.add(r);x=f[r]
            if not isinstance(x,int): return ("depends on whether the row length is odd or even",rows,extra)
            extra+=1
            if x==RH: return ("HALT after tower-long rows",rows,extra)
            r=x
    return ("still small",rows,0)
if __name__=="__main__":
    KM=int(sys.argv[1]) if len(sys.argv)>1 else 9
    for K in range(1,KM+1):
        for m in range(2,7):
            f=settled(K,m)
            for RH in range(1,m):
                v,rows,extra=follow(K,m,RH,f)
                print("round +%d store %d halt-on %d : %-48s small rows %s  tower-long rows %d"%(K,m,RH,v,rows,extra),flush=True)
