import sys
tm=sys.argv[1].split('_'); T={}
for i,s in enumerate(tm):
    for b in range(2):
        c=s[3*b:3*b+3]
        if c!='---': T[(i,b)]=(int(c[0]),1 if c[1]=='R' else -1,ord(c[2])-65)
tape={};pos=0;st=0;lo=0;ev=[]
for s in range(400000):
    b=tape.get(pos,0)
    if (st,b) not in T: print('halt',s);break
    w,d,n=T[(st,b)];tape[pos]=w;pos+=d;st=n
    if pos<lo:
        lo=pos
        if s>200000: ev.append(s)
d=[ev[i+1]-ev[i] for i in range(len(ev)-1)]
print(d[:60])
