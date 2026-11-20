"""lay2k.py K F : layout 2 engine pictures with other numbers.  round +K per cell eaten; promotion at depth 1 and 2 with a fresh block of F:
   (w, b) -> (w+K, b-1) ;  (w, empty, c) -> (F, w+2, c-1) ;  (w, empty, empty, d) -> (F, w+3, d-1)"""
import sys
K=int(sys.argv[1]);F=int(sys.argv[2]);TURNS=4;L=60;PADL=20
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
