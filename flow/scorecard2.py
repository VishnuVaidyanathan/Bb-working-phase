"""scorecard.py FILE [show] : every line of the recipe at once, for each table in FILE (first word of each line).
   Needs the programs nestc, zonec2, gatec2 in this folder and haltalive.py.  Prints the lines passed and the score."""
import sys,subprocess,os
from haltalive import check
D=os.path.dirname(os.path.abspath(__file__))
LINES=["nest 3+","tape grows","sticking word","branches 7-11","few small roads","river 7-9","next zone 1-2","two fillers",
       "fillers grow (2.15+)","halt hangs on a deep filler's exit","pieces (01, 001 or 1100)","halt can be hit","halt reads a fresh cell","that exit wire does two jobs","more than one way to the gate"]
def WAYS(tm):
    """how many different two-step ways lead into the halt's state (by the table)"""
    ent={}
    for s,x in enumerate(tm.split("_")):
        for k in (0,1): ent[(s,k)]=x[3*k:3*k+3]
    h=[sk for sk,e in ent.items() if e[2]=="Z"]
    if not h: return 0
    H=h[0][0];into=lambda st:[sk for sk,e in ent.items() if e[2] not in "Z-" and ord(e[2])-65==st]
    return sum(max(1,len(into(e[0]))) for e in into(H))
def run(prog,args,tabs):
    r=subprocess.run([os.path.join(D,prog)]+args,input="\n".join(tabs)+"\n",capture_output=True,text=True).stdout
    return {l.split()[0]:l.split()[1:] for l in r.splitlines() if l.strip()}
def score(tabs):
    n=run("nestc",["200000","1","0"],tabs);z=run("zonec2",["4000000"],tabs);g=run("gatec3",["2000000"],tabs);out={}
    for t in tabs:
        p=[]
        nd,span=(int(n[t][0]),int(n[t][1])) if t in n else (0,0)
        p.append(nd>=3);p.append(span>=100)
        if t in z:
            sm,rv,nx,fl=map(int,z[t][:4]);gr=float(z[t][5]);br=int(z[t][6]);st=int(z[t][7])
        else: sm=rv=nx=fl=br=st=0;gr=0.0
        p+=[st==1,7<=br<=11,1<=sm<=12,7<=rv<=9,1<=nx<=2,fl==2,gr>=2.15]
        if t in g: K,ex,dist,p2,p3,vis,mx,hang,jobs,p4=map(int,g[t])
        else: K=ex=dist=p2=p3=vis=mx=hang=jobs=p4=0
        p+=[hang==1,max(p2,p3,p4)>=4]
        r,why=check(t);p+=[r=="alive",r=="alive" and ("fresh" in why or "start" in why or "first" in why)]
        ways=WAYS(t) if 'WAYS' in globals() else 0
        p+=[jobs==1,(K>=2 and ex>=2) or ways>=2]
        out[t]=(sum(p),p,dict(nest=nd,small=sm,river=rv,next=nx,fillers=fl,growth=gr,branches=br,loop=K,exits=ex,visits=vis,maxrounds=mx,p01=p2,p001=p3,p1100=p4,hang=hang,jobs=jobs))
    return out
if __name__=="__main__":
    tabs=[l.split()[0] for l in open(sys.argv[1]) if l.strip()];res=score(tabs);show=len(sys.argv)>2
    for t in tabs:
        sc,p,info=res[t]
        print(t,sc,"".join("Y" if x else "." for x in p))
        if show:
            print("   passed:",", ".join(L for L,x in zip(LINES,p) if x));print("   failed:",", ".join(L for L,x in zip(LINES,p) if not x));print("   ",info)
