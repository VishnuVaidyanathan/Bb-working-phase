"""quick_sim_with_remainders.py TABLE and Quick_Sim options : runs Shawn Ligocki's Quick_Sim (not included here; set QUICK_SIM_DIR to the
   Code folder of github.com/sligocki/busy-beaver) and, at the two places where it stops with
   "Cannot mod Iterated_Math" / "Cannot divmod Iterated_Math", lets remainder.py work out the remainder exactly.
   Nothing in his code is changed on disk; the two methods are replaced while the program runs."""
import sys,os,runpy
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
QS=os.environ.get("QUICK_SIM_DIR",os.path.expanduser("~/busy-beaver/Code"));sys.path.insert(0,QS)
import remainder
import Iterated_Expression as IE
from Algebraic_Expression import substitute
count={"mod":0,"divmod":0}
LOG=os.environ.get("REMAINDER_LOG")      # optional file: every remainder asked (modulus, answer, formula)
def it_mod(self,other):
    if other==1: return 0
    m=int(other);count["mod"]+=1
    r=remainder.mod(str(self),m)
    if LOG: open(LOG,"a").write("%d\t%d\t%s\n"%(m,r,str(self)))
    return r
def unroll(it):
    """f^N(x) written as f( f^(N-1)(x) ), so that it becomes an ordinary formula with the repeated rule one level inside."""
    inner=IE.Iterated_Expression(it.step_expr,it.var,it.start_val,it.num_reps-1)
    return substitute(it.step_expr,{it.var:inner})
def math_divmod(self,other):
    if other==1: return (self,0)
    m=int(other)
    if all(t.coef%m==0 for t in self.terms):
        q,r=divmod(self.const,m)
        return (IE.Iterated_Math([IE.Iterated_Term(t.it_expr,t.coef//m) for t in self.terms],q),r)
    count["divmod"]+=1
    total=self.const
    for t in self.terms: total=total+unroll(t.it_expr)*t.coef
    return divmod(total,m)
def expr_divmod(self,other):
    if other==1: return (self,0)
    return math_divmod(IE.Iterated_Math([IE.Iterated_Term(self,1)],0),other)
IE.Iterated_Math.__mod__=it_mod
IE.Iterated_Math.__divmod__=math_divmod
IE.Iterated_Expression.__mod__=it_mod
IE.Iterated_Expression.__divmod__=expr_divmod

# A third stopping place, not about remainders: inside a formula that still has a variable in it, a power term that is itself a plain
# number has no "smallest value" recorded and Quick_Sim stops with "'ExpTerm' object has no attribute 'min_value'".
# The smallest value of a plain number is the number itself, so that is supplied here when it is asked for.
import Exp_Int as _EI
def _term_min_value(self,name):
    if name=="min_value":
        count["minval"]=count.get("minval",0)+1
        return _EI.ExpInt([self],0,1)
    if name=="vars": return set()                       # a plain number has no variables
    raise AttributeError(name)
_EI.ExpTerm.__getattr__=_term_min_value
sys.argv=[os.path.join(QS,"Quick_Sim.py")]+sys.argv[1:]
try: runpy.run_path(sys.argv[0],run_name="__main__")
finally: sys.stderr.write("remainder calculator used: %d remainders, %d divisions; smallest-value fix used %d times\n"%(count["mod"],count["divmod"],count.get("minval",0)))
