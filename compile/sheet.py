"""sheet.py SHEETFILE : turn a hand sheet (story -> transcript -> table with open choices) into every table it allows.
   Sheet lines:   A0 1RB        a fixed wire
                  A1 ?LC        ? = open (write 0/1, move L/R, or any state)
                  E0 HALT
                  ones A1 C1 E1 = 1     the listed wires together write exactly this many 1s
   Prints one table per line (halt written 1RZ).  Thought tool only."""
import sys,itertools
def tables(f):
    W={};cons=[];names=[]
    for l in open(f):
        l=l.split("#")[0].split()
        if not l: continue
        if l[0]=="ones": cons.append((l[1:-2],int(l[-1])))
        else:
            W[l[0]]=l[1]
            if l[0][0] not in names: names.append(l[0][0])
    names.sort();keys=[q+b for q in names for b in "01"];opts=[]
    for k in keys:
        w=W[k]
        if w=="HALT": opts.append(["1RZ"]);continue
        opts.append([a+b+c for a in ("01" if w[0]=="?" else w[0]) for b in ("LR" if w[1]=="?" else w[1]) for c in (names if w[2]=="?" else w[2])])
    for combo in itertools.product(*opts):
        d=dict(zip(keys,combo))
        if all(sum(d[k][0]=="1" for k in ks)==n for ks,n in cons):
            yield "_".join(d[q+"0"]+d[q+"1"] for q in names)
if __name__=="__main__":
    for t in tables(sys.argv[1]): print(t)
