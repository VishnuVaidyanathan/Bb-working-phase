"""layout2 with a cut by 3 : lay2c.py J HALT [K F]    (HALT = leftover that halts, or -1 for no halt)
   R, P, W as in layout 2.   C  cut: (w, nothing at all) -> the block, grown by J cells on the right, is cut from the right end:
   every third cell is set to 0, so it becomes pieces 110 110 ... (stores of 2); the leftover 0, 1 or 2 cells stay joined to the first piece."""
import sys
J=int(sys.argv[1]);HALT=int(sys.argv[2]);K=int(sys.argv[3]) if len(sys.argv)>3 else 2;F=int(sys.argv[4]) if len(sys.argv)>4 else 1;TURNS=4;L=60;PADL=20
def tape(head,blocks):
    cells=[0]*L;i=head+1
    for n,z in blocks:
        for _ in range(n): cells[i]=1;i+=1
        i+=z
    return "".join(("[%d]"%x) if j==head else str(x) for j,x in enumerate(cells))
for w,b,c in [(1,1,0),(1,2,0),(2,1,0),(2,2,1),(3,1,2),(1,3,1),(2,3,0),(4,2,0),(F,4,0),(F,2,2)]:
    rest=[(c,1)] if c else []
    print("S",tape(PADL,[(w,1),(b,1)]+rest),"S",tape(PADL-(K-1),[(w+K,1),(b-1,1)]+rest),2,2*(w+K)+10)
for w,c,d in [(2,1,1),(2,2,0),(3,3,0),(4,1,2),(5,2,1),(3,4,2),(6,3,0)]:
    rest=[(d,1)] if d else []
    print("S",tape(PADL,[(w,2),(c,1)]+rest),"S",tape(PADL-F-1,[(F,1),(w+2,1),(c-1,1)]+rest),TURNS,2*(w+F)+26)
for w,d,e in [(2,1,1),(2,2,0),(3,3,0),(4,1,2),(5,2,1),(7,2,0)]:
    rest=[(e,1)] if e else []
    print("S",tape(PADL,[(w,3),(d,1)]+rest),"S",tape(PADL-F-1,[(F,1),(w+3,1),(d-1,1)]+rest),TURNS,2*(w+F)+30)
for w in range(3,13):
    g=w+J;r=g%3
    if r==HALT: print("S",tape(PADL,[(w,8)]),"HALT",TURNS+1,4*w+40);continue
    cells=[1]*g
    for i in range(g-1,-1,-3): cells[i]=0
    row="".join(map(str,cells));t=[0]*L
    for i,c in enumerate(cells): t[PADL+1+i]=c
    print("S",tape(PADL,[(w,8)]),"S","".join(("[%d]"%x) if j==PADL else str(x) for j,x in enumerate(t)),TURNS+1,4*w+40)
