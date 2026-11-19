"""haltalive.py [file] : can the halt ever be hit?  A two-step check on the table alone.
   The halt is "state H reads symbol b".  H is entered by some wire e, which moves one way.  If every wire f that leads
   into e's state moves the OTHER way, then H reads the very cell f has just written.  If all those f write the symbol
   that is not b, the halt can never be hit.   Prints  table  alive|dead  and the reason.  (Reads tables from a file or stdin.)"""
import sys
def check(tm):
    ent={}
    for s,x in enumerate(tm.split("_")):
        for k in (0,1):
            e=x[3*k:3*k+3];ent[(s,k)]=e
    halts=[(s,k) for (s,k),e in ent.items() if e[2]=="Z"]
    if not halts: return "nohalt",""
    H,b=halts[0]
    into=lambda st:[(s,k) for (s,k),e in ent.items() if e[2] not in "Z-" and ord(e[2])-65==st]
    if H==0: return "alive","the halt is in the start state"
    es=into(H)
    if not es: return "dead","no wire leads to the halt's state"
    for e in es:
        me=ent[e][1];st=e[0]
        if st==0 and e[1]==0: return "alive","entered from the first step"
        fs=into(st)
        if st==0: fs=fs+[None]
        for f in fs:
            if f is None: return "alive","entered from the start state"
            if ent[f][1]==me: return "alive","%s%d then %s%d move the same way, so the halt reads a fresh cell"%("ABCDEFG"[f[0]],f[1],"ABCDEFG"[e[0]],e[1])
            if int(ent[f][0])==b: return "alive","%s%d writes %d and %s%d steps back onto it"%("ABCDEFG"[f[0]],f[1],b,"ABCDEFG"[e[0]],e[1])
    return "dead","every way in steps back onto a cell that was just written %d"%(1-b)
if __name__=="__main__":
    src=open(sys.argv[1]) if len(sys.argv)>1 else sys.stdin
    for line in src:
        t=line.split()[0] if line.strip() else ""
        if len(t)<34: continue
        r,why=check(t);print(t,r,"|",why)
