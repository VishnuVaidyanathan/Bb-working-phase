"""leadmap.py : thought experiments on Pavel Kropitz's machine.  Start it on a lead word of k ones and one lone counter c,
   and follow the canonical visits until it halts, makes a row (a list of 8 or more counters), or 400 visits pass.
   Prints one line per (k, c):  HALT / ROW n (first list of 8+ counters, with the lead word then) / the lead and counters it reached."""
import sys,rules as R
def fate(k,c,maxv=400):
    lead="%d.1"%k;cs=[c];path=[]
    for i in range(maxv):
        r=R.nxt(lead,cs,400000)
        if r=="HALT": return "HALT after %d visits"%i+("  (via "+" ".join(path[-3:])+")" if path else "")
        if r=="?": return "? (no visit of the usual form)"
        nl,ncs=r
        if nl!=lead or (len(ncs)==1 and len(cs)>1): path.append("%s:%s"%(nl,ncs[0] if len(ncs)==1 else len(ncs)))
        lead,cs=nl,ncs
        if len(cs)>=8: return "ROW of %d at lead %s"%(len(cs),lead)
    return "goes on: lead %s, %d counters"%(lead,len(cs))
if __name__=="__main__":
    K=int(sys.argv[1]) if len(sys.argv)>1 else 8;Cm=int(sys.argv[2]) if len(sys.argv)>2 else 10
    for k in range(1,K+1):
        for c in range(1,Cm+1): print("lead %d  counter %2d : %s"%(k,c,fate(k,c)),flush=True)
