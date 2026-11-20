"""rules.py : thought experiments on Jeff Ketchersid's champion.  A tape is built for a chosen (block; stores) in his layout,
   the machine is run from the home position, and the next home visit (or the halt) is read back.  Prints the event rules by case."""
import sys,homes as H
def build(w,stores):
    tape={-1:1};p=1                      # one 1 just left of home (as in the real run)
    for i in range(w): tape[p]=1;p+=1
    for s in stores:
        p+=2
        for i in range(s): tape[p]=1;p+=1
    return tape
def dec(r):
    w=r[0][0] if r else 0;st=[]
    for i,(a,b) in enumerate(r):
        if i>0: st.append(a)
        if i<len(r)-1: st+=[0]*((b-2)//2)
        if i<len(r)-1 and b%2: st.append("gap%d"%b)
    return w,st
def nxt(w,stores,maxsteps=2000000):
    h,halt=H.homes(H.J,maxsteps,tape=build(w,stores),pos=0,state="A",maxhomes=40)
    out=[dec(r) for step,left,r in h[1:] if left==1]
    if halt is not None and not out: return "HALT"
    return out[0] if out else ("HALT" if halt is not None else "?")
if __name__=="__main__":
    # where is the left 1 in the real run?
    h,_=H.homes(H.J,400000)
    print("check of the builder against the real run:",all(nxt(*dec(r))==dec(r2) for (s,l,r),(s2,l2,r2) in zip(h[30:200],h[31:201]) if l==1 and l2==1))
    for g in (1,2,3,4):
        for d in (1,2,3,4,5):
            for rest in ([],[1],[2,1],[0,1]):
                row=[]
                for w in (7,8,9,10,20,21,22,23):
                    row.append("%d:%s"%(w,nxt(w,[0]*g+[d]+rest)))
                print("g=%d payer %d rest %s | %s"%(g,d,rest," ; ".join(row)))
