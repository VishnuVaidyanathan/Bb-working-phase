"""Pavel Kropitz's 7-state machine: the decimal transcript with repeats folded, nothing else.
   python3 pavel_plain.py STEPS [out.pdf]      x(n) = x repeated n times, (word)(n) = word repeated n times"""
import re,sys
from read import load
T=load("1RB0RA_1LC1LF_1RD0LB_1RA1LE_1RZ0LC_1RG1LD_0RG0RF");H="0123456789abcd"
N=int(sys.argv[1]);tape={};p=0;s=0;d=[]
for i in range(N):
    r=tape.get(p,0);t=T[(s,r)];d.append(H[2*s+r]);tape[p]=t[0];p+=t[1];s=t[2]
S="".join(d);toks=[];i=0
while i<len(S):
    best=None
    for L in range(1,9):
        w=S[i:i+L];n=1
        while S[i+n*L:i+(n+1)*L]==w: n+=1
        if n>=(3 if L<=2 else 2) and (best is None or n*L>best[0]*best[1]): best=(n,L)
    if best:
        n,L=best;w=S[i:i+L];toks.append((w if L==1 else "("+w+")")+"(%d)"%n);i+=n*L
    else: toks.append(S[i]);i+=1
x="".join(toks)
back=re.sub(r'\(([0-9a-d]+)\)\((\d+)\)',lambda m:m.group(1)*int(m.group(2)),x)
back=re.sub(r'([0-9a-d])\((\d+)\)',lambda m:m.group(1)*int(m.group(2)),back)
assert back==S
if len(sys.argv)<3: print(x)
else:
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen import canvas
    c=canvas.Canvas(sys.argv[2],pagesize=A4);W,Hh=A4;fs=11;mx=40;width=int((W-2*mx)/(fs*0.6));lh=fs*1.5
    def head():
        c.setFont("Helvetica",8.5);c.drawString(mx,Hh-30,"Pavel Kropitz's machine 1RB0RA_1LC1LF_1RD0LB_1RA1LE_1RZ0LC_1RG1LD_0RG0RF   first %d digits   x(n) = x repeated n times"%N);c.setFont("Courier",fs)
    head();y=Hh-55;line=""
    for t in toks+[None]:
        if t is None or len(line)+len(t)>width:
            c.drawString(mx,y,line);y-=lh;line=""
            if y<40 and t is not None: c.showPage();head();y=Hh-55
        if t: line+=t
    c.save();print(len(S),"digits ->",len(x),"characters")
