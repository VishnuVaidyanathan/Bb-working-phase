"""neighbours.py TABLE : every table one wire away (the first step stays 1RB):
   - one wire changed to any other write, move and next state, the halt left where it is
   - the halt moved to another wire, and the old halt wire given any write, move and next state"""
import sys
opts=[w+m+s for w in "01" for m in "LR" for s in "ABCDEFG"]
def single(tm):
    ent=[[x[:3],x[3:]] for x in tm.split("_")];out=set()
    hs,hk=[(s,k) for s in range(7) for k in (0,1) if ent[s][k]=="1RZ"][0]
    for s in range(7):
        for k in (0,1):
            if (s,k)==(hs,hk) or (s,k)==(0,0): continue
            if ent[s][k]!="---":
                for o in opts:
                    if o!=ent[s][k]:
                        e=[r[:] for r in ent];e[s][k]=o;out.add("_".join(a+b for a,b in e))
            for o in opts:
                e=[r[:] for r in ent];e[s][k]="1RZ";e[hs][hk]=o;out.add("_".join(a+b for a,b in e))
    return out
if __name__=="__main__": print("\n".join(sorted(single(sys.argv[1]))))
