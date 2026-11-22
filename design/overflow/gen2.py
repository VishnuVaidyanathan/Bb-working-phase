import sys,itertools
J="1RB0LD_0LC0RA_1RE1LD_1LE1RF_1LF0RC_1RG0LE_---1RA"
cells=[J[q*7+b*3:q*7+b*3+3] for q in range(7) for b in (0,1)]
opts=[w+d+s for w in "01" for d in "LR" for s in "ABCDEFG"]
free=[i for i in range(14) if cells[i]!="---"]
print(J)
for k in (1,2):
    for idx in itertools.combinations(free,k):
        for vals in itertools.product(*[[o for o in opts if o!=cells[i]] for i in idx]):
            c=cells[:]
            for i,v in zip(idx,vals): c[i]=v
            print("_".join(c[2*q]+c[2*q+1] for q in range(7)))
