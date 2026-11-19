"""scorecard.py FILE [show] : every line of the recipe at once, for each table in FILE (first word of each line).
   Needs the programs nestc, zonec2, gatec2 in this folder and haltalive.py.  Prints the lines passed and the score."""
import sys,subprocess,os
from haltalive import check
D=os.path.dirname(os.path.abspath(__file__))
LINES=["nest 3+","tape grows","sticking word","branches 7-11","few small roads","river 7-9","next zone 1-2","two fillers",
       "fillers grow (2.15+)","arithmetic gate","pieces 01/001","halt can be hit","halt reads a fresh cell","gate is rare","ways out are mixed"]
def run(prog,args,tabs):
    r=subprocess.run([os.path.join(D,prog)]+args,input="\n".join(tabs)+"\n",capture_output=True,text=True).stdout
    return {l.split()[0]:l.split()[1:] for l in r.splitlines() if l.strip()}
def score(tabs):
    n=run("nestc",["200000","1","0"],tabs);z=run("zonec2",["4000000"],tabs);g=run("gatec2",["2000000"],tabs);out={}
    for t in tabs:
        p=[]
        nd,span=(int(n[t][0]),int(n[t][1])) if t in n else (0,0)
        p.append(nd>=3);p.append(span>=100)
        if t in z:
            sm,rv,nx,fl=map(int,z[t][:4]);gr=float(z[t][5]);br=int(z[t][6]);st=int(z[t][7])
        else: sm=rv=nx=fl=br=st=0;gr=0.0
        p+=[st==1,7<=br<=11,1<=sm<=12,7<=rv<=9,1<=nx<=2,fl==2,gr>=2.15]
        if t in g: K,ex,dist,p2,p3,vis,mx=map(int,g[t])
        else: K=ex=dist=p2=p3=vis=mx=0
        p+=[K>=2 and dist<=3,max(p2,p3)>=4]
        r,why=check(t);p+=[r=="alive",r=="alive" and ("fresh" in why or "start" in why or "first" in why)]
        p+=[K>=2 and 3<=vis<=300,K>=2 and ex>=2]
        out[t]=(sum(p),p,dict(nest=nd,small=sm,river=rv,next=nx,fillers=fl,growth=gr,branches=br,loop=K,exits=ex,visits=vis,maxrounds=mx,p01=p2,p001=p3))
    return out
if __name__=="__main__":
    tabs=[l.split()[0] for l in open(sys.argv[1]) if l.strip()];res=score(tabs);show=len(sys.argv)>2
    for t in tabs:
        sc,p,info=res[t]
        print(t,sc,"".join("Y" if x else "." for x in p))
        if show:
            print("   passed:",", ".join(L for L,x in zip(LINES,p) if x));print("   failed:",", ".join(L for L,x in zip(LINES,p) if not x));print("   ",info)
