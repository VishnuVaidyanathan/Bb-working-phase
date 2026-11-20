"""life2.py : the life of layout 2 with stores of 2 (cut by 3, keep 110), by arithmetic.
   T(n) = ones on the tape when a row of n stores of 2 is used up: 5, 10, 44, then T(n+1) = 4*T(n) + 4  (measured on the 5-state engine, n = 1..6).
   The cut: the block is T(n)+J cells; cut by 3 gives n' = (T+J)//3 new stores; the leftover (T+J) mod 3 is the gate."""
import sys
sys.setrecursionlimit(10000)
def Tmod(n_res,M):
    # T(n) mod M for n given as a function res(mod) -> n mod that ; T(n) = (136*4^(n-3) - 4)/3  for n>=3
    M3=3*M
    # order of 4 modulo 3M (M a power of 3 here): 4 = 1+3, order of 4 mod 3^k is 3^(k-1)
    k=0;x=M3
    while x%3==0: x//=3;k+=1
    assert x==1
    order=3**(k-1) if k>=1 else 1
    e=(n_res(order)-3)%order
    return ((136*pow(4,e,M3)-4)%M3)//3
def life(n0,J,halt,layers=14):
    out=[];cur=("exact",n0)
    def res_of(cur):
        if cur[0]=="exact": return lambda m: cur[1]%m
        return cur[1]
    for L in range(1,layers+1):
        if cur[0]=="exact" and cur[1]<3: T={1:5,2:10}[cur[1]] if cur[1]>=1 else None
        else: T=None
        if cur[0]=="exact" and cur[1]<40:
            n=cur[1];T=T if T is not None else (136*4**(n-3)-4)//3
            B=T+J;r=B%3;out.append((L,n,r))
            if r==halt: return out,L
            cur=("exact",B//3)
        else:
            rs=res_of(cur)
            r=(Tmod(rs,3)+J)%3;out.append((L,None,r))
            if r==halt: return out,L
            prev=rs
            cur=("res",(lambda prev: (lambda m: ((Tmod(prev,3*m)+J)%(3*m))//3))(prev))
    return out,None
if __name__=="__main__":
    for n0 in (1,2,3,4):
        for J in (-1,0,1,2):
            for h in (0,1,2):
                out,L=life(n0,J,h)
                print("start %d stores, block grows %+d before the cut, halt on leftover %d: leftovers by layer %s -> %s"%(n0,J,h,[r for _,_,r in out],("falls in layer %d (stores then: %s)"%(L,out[-1][1] if out[-1][1] is not None else "beyond writing")) if L else "no fall in 14 layers"))
