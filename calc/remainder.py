"""remainder.py : remainders of numbers far too big to write down.

   A number is given as a formula, the way a simulator prints it, for example
       (9 * ((λg → ((-17 + 7 * 3^(9 g + 74))/2))^((-11 + 7 * 3^92)/2) (5)) + 72)
   built from whole numbers, + - *, exact division, powers b^E, and "do this rule N times starting from X":  (λg → RULE)^(N) (X).
   mod(formula, m) gives the exact remainder on division by m.

   How it works (all standard number theory, nothing guessed):
     * b^E mod m needs only E mod L (L = Carmichael's number of m) once E is past a small threshold.
     * X/d mod m needs X mod (m*d).
     * a rule repeated N times: find a modulus M (a multiple of m) on which the rule is a plain table  r -> rule(r) mod M.
       Walk the table from the start value; the walk must fall into a loop; then only N mod (loop length) matters.
   Usage:  python3 remainder.py "FORMULA" M        or        python3 remainder.py --test"""
import sys,re
from math import gcd
sys.setrecursionlimit(100000)
EXACT_BITS=4000            # numbers up to this many bits are simply computed; beyond that they are "huge"

# ---------- reading a formula ----------
TOK=re.compile(r"\s*(λ|→|\d+|[A-Za-z_]\w*|<\w+>|[-+*/^()])")
def tokens(s):
    out=[];i=0;s=s.strip()
    while i<len(s):
        m=TOK.match(s,i)
        if not m: raise ValueError("cannot read formula at: "+s[i:i+30])
        out.append(m.group(1));i=m.end()
    return out
class P:
    def __init__(s,t): s.t=t;s.i=0
    def peek(s): return s.t[s.i] if s.i<len(s.t) else None
    def take(s,x=None):
        v=s.peek()
        if x is not None and v!=x: raise ValueError("expected %s, found %s"%(x,v))
        s.i+=1;return v
    def expr(s):
        a=s.term()
        while s.peek() in("+","-"):
            op=s.take();b=s.term();a=("add",a,b) if op=="+" else ("sub",a,b)
        return a
    def term(s):
        a=s.unary()
        while True:
            p=s.peek()
            if p=="*": s.take();a=("mul",a,s.unary())
            elif p=="/": s.take();a=("div",a,s.unary())
            elif p is not None and (p[0].isalpha() or p[0]=="<" or p=="(") and p not in("λ",) and a[0]=="num": a=("mul",a,s.unary())   # "9 g" means 9*g
            else: return a
    def unary(s):
        if s.peek()=="-": s.take();return ("neg",s.unary())
        return s.power()
    def power(s):
        a=s.atom()
        if s.peek()=="^": s.take();return ("pow",a,s.unary())
        return a
    def atom(s):
        p=s.take()
        if p is None: raise ValueError("formula ends too early")
        if p.isdigit(): return ("num",int(p))
        if p=="(":
            if s.peek()=="λ":
                s.take();v=s.take();s.take("→");f=s.expr();s.take(")");s.take("^");n=s.atom();x=s.atom()
                return ("iter",f,v,x,n)
            e=s.expr();s.take(")");return e
        if p[0].isalpha() or p[0] in "_<": return ("var",p)
        raise ValueError("unexpected "+p)
def parse(text):
    p=P(tokens(text));e=p.expr()
    if p.peek() is not None: raise ValueError("left over: "+str(p.t[p.i:p.i+5]))
    return e

# ---------- small number theory ----------
def factor(n):
    f=[];p=2
    while p*p<=n:
        k=0
        while n%p==0: n//=p;k+=1
        if k: f.append((p,k))
        p+=1
    if n>1: f.append((n,1))
    return f
def lcm(a,b): return a*b//gcd(a,b)
_car={}
def carmichael(n):
    """(L, K): for every b and every e >= K,  b^(e+L) = b^e  (mod n)."""
    if n not in _car:
        L=1;K=1
        for p,k in factor(n):
            lam=2**(k-2) if (p==2 and k>=3) else (p-1)*p**(k-1)
            L=lcm(L,lam);K=max(K,k)
        _car[n]=(L,K)
    return _car[n]

# ---------- a value that is known exactly, or known only by its remainders ----------
class Known:                      # an ordinary whole number
    def __init__(s,v): s.v=v
    def exact(s): return s.v
    def res(s,m): return s.v%m
class Huge:                       # a huge number of which only the remainder r mod M is known; asking for another modulus is recorded
    def __init__(s,r,M,asked): s.r=r;s.M=M;s.asked=asked
    def exact(s): return None
    def res(s,m):
        if s.M%m: s.asked.add(m);return 0
        return s.r%m
class Lazy:                       # a huge number given by a formula
    def __init__(s,e,env): s.e=e;s.env=env
    def exact(s): return exact(s.e,s.env)
    def res(s,m): return mod_(s.e,m,s.env)

class TooBig(Exception): pass
def _chk(v):
    if v.bit_length()>EXACT_BITS: raise TooBig()
    return v
def exact(e,env):
    """the plain value if it is small enough to compute, else None (= huge and positive)."""
    try: return _ex(e,env)
    except TooBig: return None
def _ex(e,env):
    k=e[0]
    if k=="num": return e[1]
    if k=="var":
        v=env[e[1]].exact()
        if v is None: raise TooBig()
        return v
    if k=="neg": return -_ex(e[1],env)
    if k in("add","sub","mul"):
        a=_ex(e[1],env);b=_ex(e[2],env)
        return _chk(a+b if k=="add" else a-b if k=="sub" else a*b)
    if k=="div":
        a=_ex(e[1],env);b=_ex(e[2],env)
        if a%b: raise ValueError("division is not exact")
        return a//b
    if k=="pow":
        b=_ex(e[1],env);x=_ex(e[2],env)
        if x<0: raise ValueError("negative power")
        if abs(b)>1 and x*max(1,abs(b).bit_length()-1)>EXACT_BITS: raise TooBig()
        return _chk(b**x)
    if k=="iter":
        _,f,v,x,n=e
        cur=_ex(x,env);N=_ex(n,env)
        if N>200000: raise TooBig()
        for _ in range(N): cur=_ex(f,{v:Known(cur)})
        return cur
    raise ValueError(k)

def mod_(e,m,env):
    if m==1: return 0
    k=e[0]
    if k=="num": return e[1]%m
    if k=="var": return env[e[1]].res(m)
    if k=="neg": return (-mod_(e[1],m,env))%m
    if k=="add": return (mod_(e[1],m,env)+mod_(e[2],m,env))%m
    if k=="sub": return (mod_(e[1],m,env)-mod_(e[2],m,env))%m
    if k=="mul": return (mod_(e[1],m,env)*mod_(e[2],m,env))%m
    if k=="div":
        d=exact(e[2],env)
        if d is None or d<=0: raise ValueError("can only divide by a small positive number")
        r=mod_(e[1],m*d,env)
        if r%d: raise ValueError("division by %d is not exact"%d)
        return (r//d)%m
    if k=="pow":
        b=exact(e[1],env)
        if b is None: raise ValueError("the base of a power must be a small number")
        x=exact(e[2],env)
        if x is not None: return pow(b,x,m)
        L,K=carmichael(m)                       # exponent is huge, so it is past the threshold K
        r=mod_(e[2],L,env)
        return pow(b,(r-K)%L+K,m)
    if k=="iter": return iter_mod(e,m,env)
    raise ValueError(k)

_tables={}
def table(f,v,m):
    """smallest modulus M (multiple of m) on which the rule f is a table, and the table. Valid for huge inputs."""
    key=(f,v,m)
    if key in _tables: return _tables[key]
    M=m
    while True:
        asked=set();T=[mod_(f,M,{v:Huge(r,M,asked)}) for r in range(M)]
        L=M
        for a in asked: L=lcm(L,a)
        if L==M: break
        M=L
        if M>3000000: raise ValueError("table would be too large (%d)"%M)
    _tables[key]=(M,T);return M,T
def iter_mod(e,m,env):
    _,f,v,x,n=e
    cur=exact(x,env);N=exact(n,env);k=0
    # 1. while everything is small, just do the steps
    while cur is not None and (N is None or k<N):
        nxt=exact(f,{v:Known(cur)})
        if nxt is None: break
        cur=nxt;k+=1
        if k>200000: raise ValueError("rule stays small for too long")
    if N is not None and k==N: return cur%m
    M,T=table(f,v,m)
    # 2. first value on the table
    if cur is not None: r=mod_(f,M,{v:Known(cur)});k+=1      # one step from a small number to a huge one
    else: r=mod_(x,M,env)
    # 3. walk the table until it loops
    if N is not None:
        todo=N-k
        if todo<0: raise ValueError("internal: too many steps")
    seen={};path=[]
    while r not in seen:
        if N is not None and len(path)==todo: return r%m
        seen[r]=len(path);path.append(r);r=T[r]
    mu=seen[r];pi=len(path)-mu
    if N is not None: return path[mu+(todo-mu)%pi]%m
    todo_mod=(mod_(n,pi,env)-k)%pi               # N is huge, so N-k is past the start of the loop
    return path[mu+(todo_mod-mu)%pi]%m

def mod(text_or_tree,m,env=None):
    e=parse(text_or_tree) if isinstance(text_or_tree,str) else text_or_tree
    return mod_(e,int(m),env or {})

# ---------- self test: compare with plain computing wherever plain computing is possible ----------
def selftest():
    global EXACT_BITS
    import random
    random.seed(7);bad=0;n=0
    rules=["((-5 + 7 * 3^(g + 2))/2)","(3 g + 11)","((-17 + 7 * 3^((-5 + 7 * 3^(9 g + 74))/2))/2)","(2^g + g)","((3^(2 g + 1) + 5 * 2^g + 4)/4)","(g * g + 3^g)","(6^g + 10 g)","(4 * 3^g - g)"]
    for rule in rules:
        for x in (0,1,2,5):
            for N in (0,1,2,3,7):
                text="(9 * ((λg → %s)^(%d) (%d)) + 72)"%(rule,N,x)
                EXACT_BITS=30000000
                try: true=_ex(parse(text),{})
                except (TooBig,OverflowError,MemoryError,ValueError): continue
                if true.bit_length()<200: continue
                for m in (2,3,4,5,6,7,8,9,12,16,27,36,100,97,360,1000,1024):
                    EXACT_BITS=64;_tables.clear()                 # force the "huge" path
                    got=mod(text,m);n+=1
                    if got!=true%m: bad+=1;print("WRONG",text,m,got,true%m)
    EXACT_BITS=4000
    # 2. the rule 3g+11 has a closed form, so a huge repeat count can be checked:  f^N(x) = ((2x+11)*3^N - 11)/2
    for x in (0,4,10**40+3):
        for N in (10**6+1,10**30+7,3**200):
            for m in (2,4,5,7,9,16,36,97,1000,1024):
                true=(((2*x+11)*pow(3,N,2*m)-11)%(2*m))//2%m
                got=mod("((λg → (3 g + 11))^(%d) (%d))"%(N,x),m);n+=1
                if got!=true: bad+=1;print("WRONG affine",x,N,m,got,true)
    # 3. consistency for repeat counts far beyond computing:  N steps  =  one written-out step after N-1 steps
    for rule in rules:
        for x in ("5","(3^300 + 1)"):
            for N,N1 in (("50","49"),("1000003","1000002"),("(3^200)","(3^200 - 1)"),("((-11 + 7 * 3^((-7 + 7 * 3^92)/2))/2)","((-13 + 7 * 3^((-7 + 7 * 3^92)/2))/2)")):
                a="((λg → %s)^(%s) (%s))"%(rule,N,x)
                inner="((λg → %s)^(%s) (%s))"%(rule,N1,x)
                b=re.sub(r"\bg\b",inner,rule)
                for m in (2,3,4,6,8,9,16,36,100,97,1024):
                    try: ga=mod(a,m);gb=mod(b,m)
                    except ValueError as ex:
                        if "not exact" in str(ex): continue
                        raise
                    n+=1
                    if ga!=gb: bad+=1;print("INCONSISTENT",rule,x,N,m,ga,gb)
    print("self test: %d remainders checked (plain computing, closed form, step consistency), %d wrong"%(n,bad))
    return bad==0
if __name__=="__main__":
    if sys.argv[1]=="--test": sys.exit(0 if selftest() else 1)
    print(mod(sys.argv[1],int(sys.argv[2])))
