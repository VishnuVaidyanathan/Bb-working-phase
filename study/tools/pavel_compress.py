"""Pavel Kropitz's 7-state machine: the decimal transcript, compressed.
   python3 pavel_compress.py STEPS
One line per gate visit (a line starts at digit c).  x(n) = x repeated n times.
W = cdadb6103b611025247953b6110252479  (the word that opens almost every visit)
U = b61025253(ad)(3)                   (one unit being crossed)
Lines with the same shape that follow each other are folded: the numbers that change are shown as a..b."""
import re,sys
from read import load
T=load("1RB0RA_1LC1LF_1RD0LB_1RA1LE_1RZ0LC_1RG1LD_0RG0RF");H="0123456789abcd"
N=int(sys.argv[1]);tape={};p=0;s=0;d=[]
for i in range(N):
    r=tape.get(p,0);t=T[(s,r)];d.append(H[2*s+r]);tape[p]=t[0];p+=t[1];s=t[2]
S="".join(d)
def comp(s):
    for L in (1,2,4,6,8,16):
        def rep(m):
            w=m.group(1);n=len(m.group(0))//len(w)
            return (w if len(w)==1 else "["+w+"]")+"(%d)"%n
        s=re.sub(r'((?:[0-9a-d]){%d})\1{2,}'%L,rep,s)
    return s
lines=[];st=1
for part in re.split(r'(?=c)',S):
    if not part: continue
    x=part.replace("cdadb6103b611025247953b6110252479","W ")
    x=x.replace("b61025253adadad","U")
    x=re.sub(r'(?:U){2,}',lambda m:"U(%d) "%(len(m.group(0))),x)
    x=comp(x)
    x=re.sub(r'(?<![0-9a-d(])([0-9a-d\[\]()]{5,40}?)\1{2,}',lambda m:" {"+m.group(1)+"}(%d) "%(len(m.group(0))//len(m.group(1))),x)
    x=re.sub(r'(?:52479){3,}',lambda m:"[52479](%d)"%(len(m.group(0))//5),x)
    lines.append((st,x));st+=len(part)
def shape(x): return re.sub(r'\((\d+)\)','(#)',x)
print('W = cdadb6103b611025247953b6110252479     U = b61025253(ad)(3)     x(n) = x repeated n times\n')
out=[];i=0
while i<len(lines):
    j=i
    while j+1<len(lines) and shape(lines[j+1][1])==shape(lines[i][1]): j+=1
    if j-i>=2:
        a=re.findall(r'\((\d+)\)',lines[i][1]);b=re.findall(r'\((\d+)\)',lines[j][1]);k=iter(range(len(a)))
        txt=re.sub(r'\((\d+)\)',lambda m:(lambda q:"(%s)"%a[q] if a[q]==b[q] else "(%s..%s)"%(a[q],b[q]))(next(k)),lines[i][1])
        out.append("%7d  x%-4d %s"%(lines[i][0],j-i+1,txt))
    else:
        for q in range(i,j+1): out.append("%7d        %s"%lines[q])
    i=j+1
print("\n".join(out))
