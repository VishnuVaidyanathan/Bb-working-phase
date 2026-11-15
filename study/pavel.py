import re,sys
from read import load,D
tm="1RB0RA_1LC1LF_1RD0LB_1RA1LE_1RZ0LC_1RG1LD_0RG0RF"
T=load(tm);tape={};p=0;s=0;N=int(sys.argv[1]);rows=[]
for i in range(N):
    r=tape.get(p,0)
    if s==6 and r==0:
        ks=[k for k in tape if tape[k]];lo,hi=min(ks),max(ks)
        L="".join(str(tape.get(k,0)) for k in range(lo,p));R="".join(str(tape.get(k,0)) for k in range(p+1,hi+1))
        m=re.fullmatch(r'101((100)*)101',R)
        if m:
            # left: groups (10)^m separated by single 1s
            g=[len(x)//2 for x in re.findall(r'(?:10)+',L)]
            rows.append((i,L[:4] if len(L)<5 else "",g,len(m.group(1))//3,L))
    t=T[(s,r)]
    if t is None: print("HALT",i+1);break
    tape[p]=t[0];p+=t[1];s=t[2]
prev=None
for i,_,g,k,L in rows:
    key=(tuple(g[:-3]) if len(g)>3 else ())
    if prev is None or k>=prev or len(rows)<60 or True:
        pass
    prev=k
# print compactly: only rows where k increased (a reset) or first/last of a descent
out=[];last=None
for j,(i,_,g,k,L) in enumerate(rows):
    nxt=rows[j+1][3] if j+1<len(rows) else None
    if last is None or k>last or nxt is None or nxt>k: out.append((i,g,k,L))
    last=k
for i,g,k,L in out[:60]:
    gs=str(g) if len(g)<14 else "%s ... %s (%d groups; sizes %s)"%(g[:3],g[-4:],len(g),sorted(set(g)))
    print("%9d  units right: %-6d left groups: %s   | left starts %s"%(i,k,gs,L[:8]))
