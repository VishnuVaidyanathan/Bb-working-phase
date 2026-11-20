"""fate.py ENGINE [RESTSTATE] : the fate of a layout-2 engine by arithmetic, before a machine exists.
   For a row of n equal stores (the output of a cut) the engine is run on a real tape until the fill state runs past everything;
   that gives the block B(n).  Then B(n) is shown mod 2 and mod 3: a gate on the cut's leftover is alive only if these change with n."""
import sys
def blockwhenempty(E,n,s,rest=0,maxsteps=60000000):
    T={}
    for q,x in enumerate(E.split("_")):
        for k in (0,1):
            e=x[3*k:3*k+3];T[(q,k)]=None if e[2] in 'Z-' else (int(e[0]),1 if e[1]=="R" else -1,ord(e[2])-65)
    N=3*10**6;tape=bytearray(2*N);base=N;i=base+1
    for _ in range(n):
        for _ in range(s): tape[i]=1;i+=1
        i+=1
    hi=i;p=base;st=rest;lastz=0
    for step in range(maxsteps):
        r=tape[p]
        if p>hi+6:                      # far past everything: nothing is left
            q=hi+6
            while tape[q]==1: q-=1      # skip what the fill wrote
            ones=sum(tape[base-N//2:hi+8]);return ones-(p-1-hi-6+7) if False else sum(tape[base-N//2:hi+1])
        t=T[(st,r)]
        if t is None: return None
        tape[p]=t[0];p+=t[1];st=t[2]
        if p<10 or p>2*N-10: return None
    return None
if __name__=="__main__":
    E=sys.argv[1];rest=ord(sys.argv[2])-65 if len(sys.argv)>2 else 0
    for s in (1,2,3):
        B=[blockwhenempty(E,n,s,rest) for n in range(1,10)]
        print("stores of",s,": ones on the tape when nothing is left, n=1..9:",B)
        if all(b is not None for b in B):
            print("      mod 2:",[b%2 for b in B],"  mod 3:",[b%3 for b in B],"  mod 5:",[b%5 for b in B])
