"""rules.py : thought experiments on Pavel Kropitz's machine.  A tape is built for a chosen list of counters in his own coding
   (lead word, counters of `10` separated by `110`, then `100 111` and the head on a fresh cell at the right end in state A),
   the machine is run, and the next visit of the same canonical form is read back."""
import sys,look,words,counters as C
def build(lead,cs):
    cells=[]
    if lead: a,b=map(int,lead.split("."));cells+= [1]*a+[0]*b
    for i,c in enumerate(cs):
        if i: cells+=[1,1,0]
        cells+=[1,0]*c
    cells+=[1,0,0]+[1,1,1]+[0,0,0]
    tape={i:v for i,v in enumerate(cells) if v}
    return tape,len(cells)-1
def canon(tokens):
    """(lead, [counters]) if the visit has the canonical form, else None"""
    if len(tokens)<2 or tokens[-2:]!=("1.2","3.3"): return None
    body=list(tokens[:-2]);lead=None
    if body and isinstance(body[0],str) and body[0]!="2.1": lead=body.pop(0)
    cs=[];cur=0;
    for t in body:
        if isinstance(t,int): cur=t
        elif t=="2.1": cs.append(cur);cur=0
        else: return None
    cs.append(cur)
    return lead,cs
def nxt(lead,cs,maxsteps=3000000):
    tape,pos=build(lead,cs)
    T=look.parse(look.P);st="A";lo=0;hi=pos;first=True
    for step in range(maxsteps):
        v=tape.get(pos,0)
        if st=="A" and v==0 and pos==hi and not first:
            c=canon(C.decode(words.words(tape,lo,hi)))
            if c is not None: return c
        first=False
        e=T[(st,v)]
        if e is None: return "HALT"
        tape[pos]=e[0];pos+=e[1];st=e[2]
        lo=min(lo,pos);hi=max(hi,pos)
    return "?"
if __name__=="__main__":
    # check the builder against the real run
    v=[(s,canon(c)) for s,c in C.visits(3000000) if c!="HALT"]
    v=[x for x in v if x[1] is not None]
    ok=sum(1 for (s,a),(s2,b) in zip(v[40:400],v[41:401]) if nxt(*a)==b)
    print("builder check against the real run: %d of %d canonical steps reproduced"%(ok,len(v[40:400])-0))
    for lead in ("3.1",):
        for g in (1,2,3):
            for c in (1,2,3):
                row=[]
                for b in (4,5,10,11):
                    for pre in ([],[2],[0,2]):
                        r=nxt(lead,pre+[c]+[0]*g+[b])
                        row.append("%s+[%d]+0x%d+[%d]->%s"%(pre,c,g,b,r if isinstance(r,str) else "%s%s"%(r[0] or "",r[1])))
                print(" | ".join(row)[:400])
