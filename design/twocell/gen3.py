import sys,itertools
J="1RB0RG_1RC1RB_0RD1RZ_0LE0LD_0LF1LE_1RA1LF_1LC0RB"
part=int(sys.argv[1]);cells=[J[q*7+b*3:q*7+b*3+3] for q in range(7) for b in (0,1)]
opts=[w+d+s for w in "01" for d in "LR" for s in "ABCDEFG"]
free=[i for i in range(14) if cells[i]!="1RZ"]
def emit(c): sys.stdout.write("_".join(c[2*q]+c[2*q+1] for q in range(7))+"\n")
n=0
for k in (1,2,3):
    for idx in itertools.combinations(free,k):
        for vals in itertools.product(*[[o for o in opts if o!=cells[i]] for i in idx]):
            n+=1
            if n%2!=part: continue
            c=cells[:]
            for i,v in zip(idx,vals): c[i]=v
            emit(c)
