"""Rule-level run of Jeff's machine from a clean tape  1 0 [G0] 1^P 0^g1 1^c1 0^g2 1^c2 ...
   Uses only the tested/proved move, with triplings done in one go (exact big integers).
   Returns the outcome at the first gate (a block that is a single 1)."""
import re,sys
from small import run
def parse(R):
    runs=[(c,len(m)) for c,m in ((x[0],x) for x in re.findall(r'1+|0+',R))]
    if not runs or runs[0][0]!='1': return None
    P=runs[0][1];rest=[]
    for i in range(1,len(runs)-1,2): rest.append((runs[i][1],runs[i+1][1]))
    return P,rest
def go(P,rest,maxmoves=10**6):
    log=[]
    for _ in range(maxmoves):
        if not rest: return log,"ran out of tape (outside the rule)"
        (g,Z),tail=rest[0],rest[1:]
        if g%2: return log,"odd gap (outside the rule)"
        j=g//2
        if Z==1:
            if P%2==0: return log,"gate: P even -> HALT.  P has %d digits%s"%(len(str(P)),"" if P>10**12 else " (P = %d)"%P)
            if tail: return log,"gate in the middle of the tape, P odd -> HALT.  P has %d digits"%len(str(P))
            return log,"gate at the last cell, P odd -> RESTART with (3P-1)/2 units.  P = %s"%(P if P<10**12 else "%d digits"%len(str(P)))
        if j==1:
            k=(Z-1)//2 if Z%2 else Z//2-1          # triplings before the counter is down to 1 or 2
            if k>0:
                if k>5000: return log,"tower: more than 5000 triplings in one counter (P would have over 2000 digits)"
                P=3**k*(P+3)-3; Z-=2*k; rest=[(g,Z)]+tail; log.append("tripled %d times"%k); continue
            # Z==2: one more tripling, the two gaps join
            P=3*P+6
            if not tail: return log,"ran out of tape (outside the rule)"
            rest=[(2+tail[0][0],tail[0][1])]+tail[1:]; continue
        N=3*P+8-2*j
        new=[(2,2)]*(j-2)+[(2,N)]
        if Z>2: new+=[(2,Z-2)]+tail
        elif tail: new+=[(2+tail[0][0],tail[0][1])]+tail[1:]
        else: return log,"ran out of tape (outside the rule)"
        log.append("wide gap: counter %s"%(N if N<10**9 else "%d digits"%len(str(N)))); P=2; rest=new
    return log,"not finished"
if __name__=="__main__":
    for p in range(4,17):
        d,ev,res=run(p,60000)
        clean=[(i,L,R) for i,t,L,R in ev if L=="10" and i>0 and parse(R) and len(parse(R)[1])>=1]
        if res.startswith("HALT") or not clean: print("pairs %2d: %s"%(p,res)); continue
        i,L,R=clean[0];P,rest=parse(R)
        log,out=go(P,rest)
        print("pairs %2d: first clean tape at step %d: P=%d, then %s  =>  %s"%(p,i,P,rest if len(rest)<6 else str(rest[:3])+"... %d blocks"%len(rest),out))
