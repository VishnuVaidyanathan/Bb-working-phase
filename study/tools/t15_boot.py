"""The opening of Pavel Kropitz's 6-state tower machine 1RB0LD_1RC0RF_1LC1LA_0LE1RZ_1LF0RB_0RC0RE,
   written by hand from its words, and compared with the machine."""
from read import load,D
tm="1RB0LD_1RC0RF_1LC1LA_0LE1RZ_1LF0RB_0RC0RE"
def machine(n):
    T=load(tm);tape={};p=0;s=0;o=""
    for _ in range(n):
        r=tape.get(p,0);o+=D[2*s+r];w,m,q=T[(s,r)];tape[p]=w;p+=m;s=q
    return o
def R(k): return "03"+"b93"*k+"a"+"4"*(3*k+3)+"5"      # layer round number k: the block grows by 3, the gap loses 1
def X(k): return "03"+"b93"*k+"b9245"                   # reload: the block becomes the new gap
def Y(k): return "03"+"b93"*k+"b8"                      # reload, other side
def layers(a,b): return "".join(R(k) for k in range(a,b+1))
boot=("0245168"+"a5"+R(0)                 # first pass, tiny gate
      +X(1)+"03b8"+"a5"+R(0)              # tiny reload
      +R(1)+"168"+"a5"+R(0)               # one layer, gate
      +Y(3)+"a5"+layers(0,10)+"16"        # reload, then 11 layer rounds, gate
      +"9245"+X(11)+"03b8"+"a5"+R(0)      # reload
      +R(1)+"168"+"a5"+R(0))
real=machine(len(boot))
i=next((k for k in range(len(boot)) if boot[k]!=real[k]),None)
print(len(boot),"digits, equal to the machine:",boot==real, "" if i is None else "first difference at %d: ...%s | hand %s  real %s"%(i,boot[max(0,i-10):i],boot[i:i+12],real[i:i+12]))
