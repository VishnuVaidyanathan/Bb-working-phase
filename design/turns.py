"""turns.py TABLE STATE BLOCKS [FROMSTEP TOSTEP] : thought experiment; print the tape at every head turn, with the state and the digit read."""
import sys,re
H="0123456789abcd"
def run(tm,S,blocks,a=0,b=10**9,NS=10**6,maxlines=80):
    T={}
    for s,x in enumerate(tm.split("_")):
        for k in (0,1):
            e=x[3*k:3*k+3];T[(s,k)]=None if e[2] in "Z-" else (int(e[0]),1 if e[1]=="R" else -1,ord(e[2])-65)
    right='0'+'0'.join('1'*x for x in blocks);tape={i:int(c) for i,c in enumerate(right)};p=0;s=ord(S)-65;last=0;n=0;digs=""
    for i in range(NS):
        r=tape.get(p,0);t=T[(s,r)]
        if t is None: print("stops at step",i);break
        if (t[1]!=last and last!=0) and a<=i<=b:
            ks=[k for k,v in tape.items() if v]+[p];lo=min(ks);hi=max(ks)
            row="".join(("[%d]"%tape.get(q,0)) if q==p else str(tape.get(q,0)) for q in range(lo,hi+1))
            row=re.sub(r'1{6,}',lambda m:" 1^%d "%len(m.group(0)),row)
            print("%7d %s reads %d  %-12s %s"%(i,chr(65+s),r,digs[-10:],row));n+=1;digs=""
            if n>=maxlines: break
        digs+=H[2*s+r];tape[p]=t[0];last=t[1];p+=t[1];s=t[2]
        if i>b: break
if __name__=="__main__":
    a=int(sys.argv[4]) if len(sys.argv)>4 else 0;b=int(sys.argv[5]) if len(sys.argv)>5 else 10**9
    run(sys.argv[1],sys.argv[2],[int(x) for x in sys.argv[3].split(',')],a,b)
