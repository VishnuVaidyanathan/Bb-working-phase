"""t7.py : the 7-state table 1RB1RG_1RC1RB_0LF0LD_1LC1LD_1LD0RB_0RA1LF_1RZ1RE followed by arithmetic from a blank tape.
   Rules read from its tape at home visits (design/refstack.py machine_homes), then checked against the real run:
     round:            block +3, front store -1
     front g levels empty, payer d behind:   block+3 > 2g  ->  block 2, g-1 fresh stores of 2, then (block+3-2g), payer d-1
     nothing behind:   block odd -> HALT ;  block even w -> block 2, w/2-1 stores of 2, and a last store of 4"""
import sys
sys.path.insert(0,__file__.rsplit('/',2)[0]+'/design')
import refstack,stackcalc as S,remainder as R
T7="1RB1RG_1RC1RB_0LF0LD_1LC1LD_1LD0RB_0RA1LF_1RZ1RE"
def parse(t):
    T={}
    for q,row in enumerate(t.split('_')):
        for b in (0,1):
            e=row[b*3:b*3+3];T[(chr(65+q),b)]=None if e[2]=='Z' else (int(e[0]),1 if e[1]=='R' else -1,e[2])
    return T
def model(maxhomes):
    w=0;stores=[];out=[]
    while len(out)<maxhomes:
        while stores and stores[-1]==0: stores.pop()
        out.append((w,tuple(stores)))
        if not stores:
            if w==0: w=4;continue                        # the very first step from the blank tape (observed)
            if w%2: out.append("HALT");return out
            stores=[2]*(w//2-1)+[4];w=2;continue
        if stores[0]>0: w+=3;stores[0]-=1;continue
        g=0
        while stores[g]==0: g+=1
        avail=w+3
        if avail<=2*g: out.append("SMALL BLOCK CASE (not modelled)");return out
        stores=[2]*(g-1)+[avail-2*g,stores[g]-1]+stores[g+1:];w=2
    return out
if __name__=="__main__":
    steps=int(sys.argv[1]) if len(sys.argv)>1 else 30000000
    real=refstack.machine_homes(parse(T7),0,maxsteps=steps,maxhomes=10**7)
    mod=model(len(real))
    same=sum(1 for a,b in zip(real,mod) if a==b)
    print("home visits in %d steps: %d ; arithmetic agrees on %d of them%s"%(steps,len(real),same,"" if same==len(real) else "  FIRST DIFFERENCE at %d"%next(i for i,(a,b) in enumerate(zip(real,mod)) if a!=b)))
    # the big row: block 2, 423 stores of 2, one store of 4
    row=[c for c in real if c!="HALT" and len(c[1])>100][0]
    print("big row: block %d, %d stores (%d of size 2, last %d)"%(row[0],len(row[1]),row[1].count(2),row[1][-1]))
    D=S.Design(3,2);W=D.row_end(row[0],list(row[1]))
    for M in (2,4,8):
        print("block at the end of the big row, remainder by %d: %d"%(M,R.mod_(W,M,{})))
