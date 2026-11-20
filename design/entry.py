"""entry.py : our tripwire tower by arithmetic.  For every possible first layer (start state D or E, k tickets) follow the gate rule
   k = 5q + r  ->  a*2^q - c   until a layer ends with the road b3 (the tripwire: halt).  Shows how the size of the fall depends on where the machine enters."""
rule={('D',0):(10,6,'D',1),('D',1):(10,5,'E',0),('D',2):(20,9,'E',1),('D',3):(20,9,'D',0),('D',4):(20,6,'E',0),
      ('E',0):(12,9,'D',0),('E',1):(12,6,'E',0),('E',2):(12,6,'D',1),('E',3):(12,5,'E',0),('E',4):(24,9,'E',1)}
def life(s,k):
    out=[];exact=True;m20=None
    for L in range(1,14):
        r=(k if exact else m20)%5;a,c,ns,b=rule[(s,r)];out.append(k if exact else None)
        if b: return L,out
        if exact and k//5<=2000000: k=a*2**(k//5)-c
        else:
            q4=(((k if exact else m20)-r)//5)%4;m20=(a*pow(2,q4+4,20)-c)%20;exact=False
        s=ns
    return None,out
def show(x):
    if x is None: return "beyond writing"
    return str(x) if x<10**13 else "about 2^%d"%x.bit_length()
if __name__=="__main__":
    rows=[]
    for s in "DE":
        for k in range(1,201):
            L,o=life(s,k)
            if L: rows.append((sum(1 for x in o if x is None),max(x.bit_length() for x in o if x is not None),s,k,L,o))
    rows.sort()
    print("largest falls (tickets in each layer; the last layer is where it falls):")
    for nb,bl,s,k,L,o in rows[-12:]: print("  first layer %s with %3d tickets, falls in layer %d: %s"%(s,k,L," -> ".join(show(x) for x in o)))
    print("our machine enters at E with 1 ticket:"," -> ".join(show(x) for x in life('E',1)[1]))
    import collections
    c=collections.Counter((nb,L) for nb,bl,s,k,L,o in rows)
    print("how many first layers (of 400) give a fall whose last layers are beyond writing:",{k:v for k,v in sorted(c.items())})
