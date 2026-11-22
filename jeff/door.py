"""door.py : one payment (ticket g=1) of Jeff Ketchersid's champion, written as the order in which wires fire, with the tape shown
   each time the head leaves the 9 round wires.  Shows how a payment is made of round wires plus a few 'door' wires.
   Thought tool; credit for the machine: Jeff Ketchersid."""
import homes as H,model as M
T=H.parse(H.J);ROUND={"A0","B0","B1","C0","D0","D1","E0","E1","F0"}
tape={};pos=0;st="A";hi=0;lo=0;seq=[];prev=None;want=3;seen=0
def show():
    return "".join("1" if tape.get(i,0) else "." for i in range(lo,min(hi+2,lo+60)))+"   head at %d in %s"%(pos-lo,st)
def read():
    runs=[];q=pos+1
    while q<=hi+1:
        a=0
        while tape.get(q,0): a+=1;q+=1
        b=0
        while q<=hi+1 and not tape.get(q,0): b+=1;q+=1
        runs.append((a,b))
    if runs and runs[-1][0]==0: runs.pop()
    return M.dec(runs),sum(tape.get(i,0) for i in range(lo,pos))
for s in range(3000000):
    v=tape.get(pos,0)
    if st=="A" and v==0:
        c,left=read()
        if left==1:
            if prev is not None:
                stz=list(prev[1])
                if stz and stz[0]==0 and len(stz)>1 and stz[1]>=2:
                    seen+=1
                    if seen==want:
                        print("before:",prev,"\nafter: ",c,"\n")
                        out=[];
                        for w,snap in seq:
                            if out and out[-1][0]==w and snap is None: out[-1][1]+=1
                            else: out.append([w,1,snap])
                        line=[]
                        for w,k,snap in out:
                            if snap:
                                if line: print("   round wires:"," ".join(line));line=[]
                                print("DOOR",w,H.J.split("_")["ABCDEFG".index(w[0])][int(w[1])*3:int(w[1])*3+3],"x%d"%k if k>1 else "","  tape:",snap)
                            else: line.append(w+("x%d"%k if k>1 else ""))
                        if line: print("   round wires:"," ".join(line))
                        break
            prev=c;seq=[]
    w=st+str(v);e=T[(st,v)]
    seq.append((w,None if (w in ROUND or (seq and seq[-1][0]==w)) else show()))
    tape[pos]=e[0];pos+=e[1];st=e[2];hi=max(hi,pos);lo=min(lo,pos)
