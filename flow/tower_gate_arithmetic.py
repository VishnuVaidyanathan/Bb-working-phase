"""tower_gate_arithmetic.py : the gate of the tower machine 1RB1LE_1LE1LD_1RZ1LG_1RF0LB_1RC1LA_1RA1RB_0RD1RG written as arithmetic.
   A layer starts in state D or E with k tickets (stripes).  With k = 5q + r the next layer has a*2^q - c tickets.
   The ten (start, r) rules were read off 84 thought experiments made with layer.c and are checked here against all of them.
   Then the rule is followed layer by layer from the real run (4 tickets, start E) to see when each case first happens."""
# the tower machine's gate as arithmetic.  rule[(start,r)] = (a, c, next start, uses b3)   next k = a*2^q - c,  k = 5q + r
rule={('D',0):(10,6,'D',1),('D',1):(10,5,'E',0),('D',2):(20,9,'E',1),('D',3):(20,9,'D',0),('D',4):(20,6,'E',0),
      ('E',0):(12,9,'D',0),('E',1):(12,6,'E',0),('E',2):(12,6,'D',1),('E',3):(12,5,'E',0),('E',4):(24,9,'E',1)}
import re
# check the rule against every thought experiment
bad=0
for l in open(__file__.rsplit('/',1)[0]+'/tower_gate_84_thought_experiments.txt'):
    m=re.match(r'K=(\d+) start=(\w) -> K=(\d+) state=(\w) steps=(\d+) b3=(\d+)',l);k=int(m.group(1));s=m.group(2)
    a,c,ns,b=rule[(s,k%5)]
    if (a*2**(k//5)-c,ns,b)!=(int(m.group(3)),m.group(4),min(1,int(m.group(6)))): bad+=1
print("thought experiments that disagree with the rule:",bad,"of 84")
s,k='E',4;exact=True;seen={};out=[]
for layer in range(2,40):
    r=k%5;out.append((layer,s,r,k if exact else None,k%20,rule[(s,r)][3]));key=(s,k%20)
    a,c,ns,b=rule[(s,r)]
    if exact and k<3000000:
        k=a*2**(k//5)-c
    else:
        exact=False;q4=((k-r)//5)%4 if isinstance(k,int) else None
        k=(a*pow(2,q4+4,20)-c)%20    # q is huge here, so 2^q mod 20 depends only on q mod 4
    s=ns
first={}
for layer,s,r,k,m,b3 in out:
    first.setdefault((s,r),layer)
    if layer<=16: print("layer %2d starts %s, tickets mod 5 = %d, ends %s, %s"%(layer,s,r,"with b3" if b3 else "plain  ",("tickets = %d"%k if k is not None and k<10**8 else ("tickets is about 2^%d"%k.bit_length() if k is not None else "tickets beyond writing, mod 20 = %d"%m))))
print("first layer where each of the 10 cases happens:")
for key in sorted(rule): print("  start %s, remainder %d : %s"%(key[0],key[1],first.get(key,"never in 38 layers")))
