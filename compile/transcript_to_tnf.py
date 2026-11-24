"""transcript_to_tnf.py TABLE N  (or: DIGITS given with -d "0 2 4 ...") : which tables give this transcript?
   Takes the first N digits of TABLE's run from a blank tape (digits: A0=0 A1=1 B0=2 ... G0=c G1=d), then forgets the table
   and asks: how many tables produce exactly these N digits?  A digit names the state and the symbol read, so each wire's next
   state is read off the next digit; what the wire writes and which way it moves must be found - the tool tries every choice
   and keeps those that reproduce the digits.  Prints, per wire, what is forced and what is still open.  Thought tool only."""
import sys
D="0123456789abcd"
def digits_of(t,n):
    rows=t.split("_");T={}
    for q,r in enumerate(rows):
        for b in (0,1):
            e=r[b*3:b*3+3];T[(q,b)]=None if e[2] in "-Z" else (int(e[0]),1 if e[1]=="R" else -1,ord(e[2])-65)
    tape={};pos=0;st=0;out=[]
    for k in range(n):
        v=tape.get(pos,0);e=T[(st,v)]
        if e is None: out.append(st*2+v);break
        out.append(st*2+v);tape[pos]=e[0];pos+=e[1];st=e[2]
    return out
def solve(seq):
    n=len(seq);sols=[];nx={}
    for a,b in zip(seq,seq[1:]):          # a wire has one next state: the digit after it must always be of that state
        if nx.setdefault(a,b//2)!=b//2: return []
    def go(k,tape,pos,wm):
        if k==n: sols.append(dict(wm));return
        w=seq[k]
        if tape.get(pos,0)!=w%2: return
        if k==n-1:                       # last digit: only the read is checked
            sols.append(dict(wm));return
        if w in wm: choices=[wm[w]]
        else: choices=[(a,m) for a in (0,1) for m in (-1,1)]
        for a,m in choices:
            new=w not in wm
            if new: wm[w]=(a,m)
            old=tape.get(pos,0);tape[pos]=a
            go(k+1,tape,pos+m,wm)
            tape[pos]=old
            if new: del wm[w]
    go(0,{},0,{})
    return sols
def report(seq,states=7):
    sols=solve(seq);used=sorted(set(seq[:-1]));nxt={}
    for a,b in zip(seq,seq[1:]): nxt[a]=b//2
    print("digits:"," ".join(D[x] for x in seq))
    print("wires whose action is seen (fired before the last digit): %d of %d"%(len(used),2*states))
    print("ways to choose write and move for those wires that reproduce the digits:",len(sols))
    for w in range(2*states):
        name="ABCDEFG"[w//2]+str(w%2)
        if w in used:
            opts=sorted({("%d%s"%(s[w][0],"R" if s[w][1]>0 else "L"))+"ABCDEFG"[nxt[w]] for s in sols})
            print("   %s (digit %s): %s"%(name,D[w]," or ".join(opts)))
        elif w==seq[-1]: print("   %s (digit %s): fired last - what it does is not seen yet"%(name,D[w]))
        else: print("   %s (digit %s): never fired - free"%(name,D[w]))
    return sols
if __name__=="__main__":
    if sys.argv[1]=="-d": seq=[D.index(x) for x in sys.argv[2].split()]
    else: seq=digits_of(sys.argv[1],int(sys.argv[2]))
    report(seq)
