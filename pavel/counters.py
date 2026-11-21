"""counters.py : Pavel Kropitz's machine read as a list of counters at each visit (state A on a fresh cell at the right end).
   A counter = number of words `10` in a row.  Everything else is a marker, written ones.zeros (2.1 = `110`, 1.2 = `100`, ...)."""
import sys,look,words
def visits(n,maxv=10**9,tm=look.P):
    T=look.parse(tm);tape={};pos=0;st="A";lo=hi=0;out=[]
    for step in range(n):
        v=tape.get(pos,0)
        if st=="A" and v==0 and pos==hi:
            out.append((step,decode(words.words(tape,lo,hi))))
            if len(out)>=maxv: break
        e=T[(st,v)]
        if e is None: out.append((step,"HALT"));break
        tape[pos]=e[0];pos+=e[1];st=e[2]
        lo=min(lo,pos);hi=max(hi,pos)
    return out
def decode(ws):
    out=[];i=0
    while i<len(ws):
        if ws[i]==(1,1):
            j=i
            while j<len(ws) and ws[j]==(1,1): j+=1
            out.append(j-i);i=j
        else:
            a,b=ws[i];out.append("%d.%d"%(a,b));i+=1
    return tuple(out)
def shape(c): return " ".join("n" if isinstance(x,int) else x for x in c)
if __name__=="__main__":
    n=int(sys.argv[1]) if len(sys.argv)>1 else 3000000
    v=visits(n)
    from collections import Counter
    # the right end of the list (last 6 items) as a shape, and how often each follows which
    tail=Counter();trans=Counter()
    prev=None
    for step,c in v:
        if c=="HALT": break
        t=shape(c[-6:])
        tail[t]+=1
        if prev is not None: trans[(prev,t)]+=1
        prev=t
    print(len(v),"visits; different right-end shapes:",len(tail))
    for t,k in tail.most_common(14): print("%7d  ...%s"%(k,t))
