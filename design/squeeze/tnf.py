import sys
def tnf(t,start="A",steps=3000000):
    rows=t.split("_");n=len(rows);T={}
    for q,r in enumerate(rows):
        for b in (0,1):
            e=r[b*3:b*3+3];T[(q,b)]=None if e[2] in "-Z" else (int(e[0]),e[1],ord(e[2])-65)
    s0=ord(start)-65
    def run(Tb,st,steps):
        tape={};pos=0;order=[st];used=set()
        for k in range(steps):
            v=tape.get(pos,0);used.add((st,v));e=Tb[(st,v)]
            if e is None: return order,used,("HALT",k),tape
            tape[pos]=e[0];pos+=1 if e[1]=="R" else -1;st=e[2]
            if st not in order: order.append(st)
        return order,used,(sum(tape.values()),abs(pos),st),tape
    # first move must be right: mirror if needed
    first=T[(s0,0)]
    M=T if first[1]=="R" else {k:(None if v is None else (v[0],"R" if v[1]=="L" else "L",v[2])) for k,v in T.items()}
    order,used,fin,_=run(M,s0,steps)
    order+= [q for q in range(n) if q not in order]
    new={old:i for i,old in enumerate(order)}
    out=[]
    for old in order:
        s=""
        for b in (0,1):
            e=M[(old,b)]
            s+=("---" if (old,b) not in used else "1RZ") if e is None else ("---" if (old,b) not in used else "%d%s%s"%(e[0],e[1],chr(65+new[e[2]])))
        out.append(s)
    return "_".join(out),fin,len(used)
if __name__=="__main__":
    t,fin,u=tnf(sys.argv[1],sys.argv[2] if len(sys.argv)>2 else "A");print(t,"| ones, distance, state after 3M steps:",fin,"| wires used",u)
