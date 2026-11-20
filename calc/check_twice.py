"""check_twice.py LOGFILE : second route for every remainder in a log written by quick_sim_with_remainders.py (REMAINDER_LOG).
   Every "rule repeated N times" is rewritten as "one written-out step after N-1 times" (so the answer comes through the power rule
   instead of the table walk), for the asked modulus and for 4 and 8 times it. Also prints the parity of start value and repeat count."""
import sys,remainder as R
def subst(e,v,w):
    if e[0]=="var": return w if e[1]==v else e
    if e[0]=="num": return e
    if e[0]=="iter":
        _,f,vv,x,n=e
        return ("iter",f if vv==v else subst(f,v,w),vv,subst(x,v,w),subst(n,v,w))
    return (e[0],)+tuple(subst(a,v,w) if isinstance(a,tuple) else a for a in e[1:])
def unroll(e,top=True):
    if not isinstance(e,tuple) or e[0] in("num","var"): return e
    if e[0]=="iter":
        _,f,v,x,n=e
        return subst(f,v,("iter",f,v,x,("sub",n,("num",1))))
    return (e[0],)+tuple(unroll(a) for a in e[1:])
def iters(e,out):
    if isinstance(e,tuple):
        if e[0]=="iter": out.append(e)
        for a in e[1:]: iters(a,out)
    return out
bad=0;n=0
for line in open(sys.argv[1]):
    m,r,text=line.rstrip("\n").split("\t");m=int(m);r=int(r);e=R.parse(text);u=unroll(e)
    for mm in (m,4*m,8*m,3*m):
        a=R.mod(e,mm);b=R.mod(u,mm);n+=1
        if a!=b or (mm==m and a!=r): bad+=1;print("DISAGREE",mm,a,b,r)
    for it in iters(e,[])[:1]:
        print("  modulus %d answer %d | outer rule: start value mod 2 = %d, repeat count mod 2 = %d"%(m,r,R.mod(it[3],2),R.mod(it[4],2)))
print("%s: %d checks by the second route, %d disagree"%(sys.argv[1].split('/')[-1],n,bad))
