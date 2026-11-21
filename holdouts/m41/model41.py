"""model41.py : M41 as rewriting rules on the right end of its token list, checked against the real machine.
   Tokens: a number = a counter (that many words `10`); "|" = separator `100`; "1.3","1.4","1.5" = a 1 followed by 3, 4, 5 zeros.
   Rules (b, B = last counter; missing counter = 0):
     A   a | b |          (a >= 1)   ->  a-1 | b+2 |                      transfer
     B   | | b |                     ->  1.3 b+2 |
     C   c 1.3 b |        (c >= 1)   ->  c-1 | b+1 | |
     D   1.3 1.3 b |                 ->  1.4 b+1 | |
     E   M | b |   (M = 1.3 or 1.4)  ->  M widened by one zero, b+2 |
     F   | 1.5 B |                   ->  1.3 B-1 | | | |          (one separator of the row is used up)
         n 1.5 B |        (n >= 1)   ->  n-1 | B-1 | | | |
         1.5 B |          (alone)    ->  B-1 | | | |
     G   c 1.4 B |        (c >= 1)   ->  c-1 | B | | |
         | 1.4 B |                   ->  1.3 B | | |
     H   | 1.3 b |                   ->  1.3 b+1 | |
     I   B |              (alone)    ->  2 and B+2 separators            (the row)
     J   | B | (alone) -> B+2 | ;   1.3 B | (alone) -> B+1 | |
     K   1.4 B | (alone) -> B | | |          L   1.3 1.4 B |  ->  1.4 B | | |"""
import sys
def num(x): return isinstance(x,int)
def step(t,fast=False):
    """one D visit to the next; None if no rule applies"""
    t=list(t);n=len(t)
    if n<2 or t[-1]!="|": return None
    def put(prefix,c,rest):                      # a counter that reached 0 is simply not written
        return prefix+([c] if c else [])+rest
    # last counter b (may be missing)
    if num(t[-2]): b=t[-2];h=t[:-2]
    else: b=0;h=t[:-1]
    # h = everything before the last counter
    if not h:                                     # B | alone
        return [2]+["|"]*(b+2)
    if h[-1]=="|":
        g=h[:-1]
        if g and num(g[-1]):                      # A  transfer
            a=g[-1]
            if fast: return g[:-1]+["|",b+2*a,"|"]
            return put(g[:-1],a-1,["|",b+2,"|"])
        if g and g[-1]=="|": return g[:-1]+["1.3",b+2,"|"]                 # B
        if g and g[-1] in("1.3","1.4"): return g[:-1]+["1.%d"%(int(g[-1][2:])+1),b+2,"|"]   # E
        if not g: return [b+2,"|"]                                        # J  | B | alone
        return None
    m=h[-1]
    if m=="1.3":
        g=h[:-1]
        if g and num(g[-1]): return put(g[:-1],g[-1]-1,["|",b+1,"|","|"])    # C
        if g and g[-1]=="1.3": return g[:-1]+["1.4",b+1,"|","|"]             # D
        if g and g[-1]=="|": return g[:-1]+["1.3",b+1,"|","|"]               # H
        if not g: return [b+1,"|","|"]                                       # J
        return None
    if m=="1.4":
        g=h[:-1]
        if g and num(g[-1]): return put(g[:-1],g[-1]-1,["|",b,"|","|","|"])  # G
        if g and g[-1]=="|": return g[:-1]+["1.3",b,"|","|","|"]
        if g and g[-1]=="1.3": return g[:-1]+["1.4",b,"|","|","|"]            # L  (the 1.3 before it is used up)
        if not g: return ([b] if b else [])+["|","|","|"]                     # K  1.4 B | alone
        return None
    if m=="1.5":
        g=h[:-1]
        if g and num(g[-1]): return put(g[:-1],g[-1]-1,["|"])+([b-1] if b-1 else [])+["|"]*4
        if g and g[-1]=="|": return g[:-1]+["1.3"]+([b-1] if b-1 else [])+["|"]*4
        if not g: return ([b-1] if b-1 else [])+["|"]*4
        return None
    return None
if __name__=="__main__":
    import read41 as R,rules41 as Q
    seqs=[[c for s,st,c in [(s,st,Q.dec(ws)) for s,st,ws in R.visits(int(sys.argv[1]) if len(sys.argv)>1 else 3000000)] if st=="D"]]
    for lead in ([2,"|"],[1],[],[3,"|","|"]):
        for c in (0,1,2,3):
            for a in (0,1,3):
                for b in (2,5):
                    toks=lead+["1.3"]+([c] if c else [])+["|"]+([a] if a else [])+["|",b,"|"]
                    seqs.append([x for s,st,x in Q.run(toks,maxsteps=150000,maxv=4000) if st=="D"])
    ok=bad=norule=0;firstbad=None;missing={}
    for seq in seqs:
        for a,b in zip(seq,seq[1:]):
            m=step(a)
            if m is None:
                norule+=1;missing.setdefault(tuple("n" if num(x) else x for x in a[-5:]),(a,b))
            elif m==b: ok+=1
            else:
                bad+=1
                if firstbad is None: firstbad=(a,m,b)
    print("steps compared (real run and %d thought experiments): %d agree, %d differ, %d have no rule yet"%(len(seqs)-1,ok,bad,norule))
    if firstbad: print("first difference: before %s | model %s | machine %s"%tuple(Q.pack(x) for x in firstbad))
    for k,(a,b) in list(missing.items())[:8]: print("no rule for end [%s]: %s -> %s"%(" ".join(k),Q.pack(a)[-60:],Q.pack(b)[-60:]))
