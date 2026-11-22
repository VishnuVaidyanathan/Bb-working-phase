import sys
sys.path.insert(0,"/home/claude/bb-working-phase/calc")
import learn2 as L
def homes(t,block,stores,n=400000,maxh=22,start="A"):
    T=L.parse(t);cells=[0]+[1]*block
    for s in stores: cells+= [0]+[1]*s
    tape={i:v for i,v in enumerate(cells) if v};pos=0;st=start;out=[]
    for k in range(n):
        v=tape.get(pos,0)
        if (st,v)==("A",0):
            ks=[p for p,x in tape.items() if x and p>pos];left=sum(1 for p,x in tape.items() if x and p<pos)
            runs=[]
            if ks:
                q=pos+1;end=max(ks)
                while q<=end:
                    a=0
                    while tape.get(q,0): a+=1;q+=1
                    z=0
                    while q<=end and not tape.get(q,0): z+=1;q+=1
                    runs.append(str(a));runs+=["0"]*(z-1)
            out.append("(%s; %s)%s"%(runs[0] if runs else "-"," ".join(runs[1:]),"" if not left else "[%d left]"%left))
            if len(out)>=maxh: break
        e=T[(st,v)]
        if e is None: out.append("STOP %s%d at step %d"%(st,v,k));break
        tape[pos]=e[0];pos+=e[1];st=e[2]
    return out
if __name__=="__main__":
    t=sys.argv[1]
    for cfg in ((0,[]),(4,[4,4,3]),(6,[0,4,3]),(6,[0,0,4,4])):
        print("  from block %d stores %s:"%cfg," -> ".join(homes(t,*cfg))[:900])
