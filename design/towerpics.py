"""towerpics.py HALTTYPE [MAXW] : pictures of OUR tower machine (found by us, state C unused) cut into short pieces between rests
   (a rest = every time digit c is read: the right-going walk has just met a 0), plus one change made by hand:
   a layer whose ending is of type HALTTYPE (what is left at the gate on the last visit; see flow/tower_gate_arithmetic.py)
   must HALT at its last gate visit instead of going on.  HALTTYPE = -1: no halt picture (to test the tool finds the tower back)."""
import sys,re
H="0123456789abcd"
TW='1RB1LE_1LE1LD_1RZ1LG_1RF0LB_1RG1LA_1RA1RB_0RD1RG'
HT=int(sys.argv[1]);MAXW=int(sys.argv[2]) if len(sys.argv)>2 else 110
T={}
for s,x in enumerate(TW.split("_")):
    for k in (0,1):
        e=x[3*k:3*k+3];T[(s,k)]=None if e[2] in "Z-" else (int(e[0]),1 if e[1]=="R" else -1,ord(e[2])-65)
def rests(state,right,maxsteps,stop_after_layer=True):
    # returns list of (state, tape dict, head, next digit, turns since last rest, steps since last rest, lo, hi)
    tape={i:int(c) for i,c in enumerate(right)};p=0;s=ord(state)-65;out=[];turns=0;lastdir=0;steps=0;lo=hi=0;prev='';first=True;started=False
    for i in range(maxsteps):
        r=tape.get(p,0);d=H[2*s+r]
        if first or d=='c':
            out.append([s,dict(tape),p,None,turns,steps,lo,hi]);turns=0;lastdir=0;steps=0;lo=hi=p;first=False
        elif out and out[-1][3] is None and steps==1: out[-1][3]=d       # digit read just after the rest
        if stop_after_layer and prev+d in ("36","28") and i>3:
            ks=[k for k,v in tape.items() if v]
            if p==min(ks)-1:
                ts="".join(str(tape.get(q,0)) for q in range(min(ks),max(ks)+1))
                if re.fullmatch(r'(?:10)+1111',ts): out.append([s,dict(tape),p,'end',turns,steps,lo,hi]);break
        t=T[(s,r)]
        if t is None: break
        tape[p]=t[0]
        if lastdir and t[1]!=lastdir: turns+=1
        lastdir=t[1];p+=t[1];s=t[2];prev=d;steps+=1;lo=min(lo,p);hi=max(hi,p)
    return out
def pics(R,halt_at=None):
    out=[]
    for a,b in zip(R,R[1:]):
        ks=[k for k,v in a[1].items() if v]+[k for k,v in b[1].items() if v]+[a[2],b[2],b[6],b[7]]
        lo=min(ks)-1;hi=max(ks)+1
        if hi-lo+1>MAXW: continue
        f=lambda tp,h:"".join(("[%d]"%tp.get(q,0)) if q==h else str(tp.get(q,0)) for q in range(lo,hi+1))
        if halt_at is not None and a is halt_at:
            out.append("%s %s HALT %d %d"%(chr(65+a[0]),f(a[1],a[2]),6,80));break
        out.append("%s %s %s %s %d %d"%(chr(65+a[0]),f(a[1],a[2]),chr(65+b[0]),f(b[1],b[2]),b[4]+0,b[5]+2))
    return out
all_=[]
NOBLANK=len(sys.argv)>3 and sys.argv[3]=='noblank'
if not NOBLANK: all_+=pics(rests('A','0',2600,stop_after_layer=False))            # from the blank tape: the opening, layers 1 and 2, the start of layer 3
for k in range(3,11):
    for st in "DE":
        ty=(k%5-(2 if st=="E" else 0))%5
        R=rests(st,'0'+'10'*k+'1111',400000)
        if not R or R[-1][3]!='end': continue
        halt_at=None
        if ty==HT:
            gates=[x for x in R if x[3]=='6']
            if len(gates)>=2: halt_at=gates[-2]
        all_+=pics(R,halt_at)
all_=list(dict.fromkeys(all_))
print("\n".join(all_))
print("# pictures",len(all_),"halt pictures",sum(1 for x in all_ if ' HALT ' in x),file=sys.stderr)
