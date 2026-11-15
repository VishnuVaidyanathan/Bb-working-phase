"""Run Shawn Ligocki's Quick_Sim on D1, pause when the boot has laid its stack, change the stack, and continue.
   The stack on the tape at that moment is:   01 11 (10)^4 11 (10)^3 11 (01)^8
   usage: python3 from_tape.py "4,3"            -> counters (first, second), block left as 8
          python3 from_tape.py "4,3" 8          -> block
          python3 from_tape.py "4,4,3"          -> one more counter in the stack (a copy of the 10^x 11 pair)"""
import sys,os,re,runpy,time,copy,signal
QS=os.environ.get("QUICK_SIM_DIR", os.path.expanduser("~/busy-beaver/Code"))   # the Code folder of sligocki/busy-beaver
sys.path.insert(0,QS); os.chdir(QS)
TM="1RB1RD_1LC0RD_0LG1LD_1RA0RE_1LF1LA_0LC1LE_1RZ0LE"
stack=[int(x) for x in sys.argv[1].split(",")]; block=int(sys.argv[2]) if len(sys.argv)>2 else 8; limit=int(sys.argv[3]) if len(sys.argv)>3 else 120
argv=sys.argv; sys.argv=["Quick_Sim.py","-r","--exp-linear-rules","--exp-meta-linear-rules","--no-steps","--manual","--quiet",TM]
import io,contextlib
buf=io.StringIO()
with contextlib.redirect_stdout(buf):
    g=runpy.run_path(os.path.join(QS,"Quick_Sim.py"),run_name="__main__")
sim=g["sim"]; TMmod=g["Turing_Machine"]
want=re.compile(r"01\^1 11\^1 10\^4 11\^1 10\^3 11\^1 01\^8 ")
ok=False
for _ in range(200000):
    s=sim.tape.print_with_state(sim.state)
    if want.search(s): ok=True;break
    sim.step()
    if sim.op_state!=TMmod.RUNNING: break
if not ok: print("did not reach the boot tape"); sys.exit(1)
L=sim.tape.tape[0]
names=[x.to_string(False,False) for x in L]
# L is far-to-near:  0^inf, 01^1, 11^1, 10^4, 11^1, 10^3, 11^1, 01^8, ...
i4=names.index("10^4"); i3=names.index("10^3"); i8=names.index("01^8")
sep=L[i4+1]
first,last=stack[0],stack[-1]
L[i4].num=first; L[i3].num=last; L[i8].num=block
extra=[]
for v in stack[1:-1]:
    a=copy.deepcopy(L[i4]); a.num=v; extra+= [a,copy.deepcopy(sep)]
if len(stack)==1:
    del L[i4:i4+2]
else:
    L[i4+2:i4+2]=extra
for attr in ("past_configs",):
    if hasattr(sim.prover,attr):
        try: getattr(sim.prover,attr).clear()
        except Exception: pass
start_tape=sim.tape.print_with_state(sim.state)
def bye(*a): raise TimeoutError()
signal.signal(signal.SIGALRM,bye); signal.alarm(limit)
t0=time.time(); res="no answer in %d s"%limit
try:
    while sim.op_state==TMmod.RUNNING:
        sim.loop_run(1000)
    res="HALT" if sim.op_state in (TMmod.HALT,TMmod.UNDEFINED) else ("runs forever" if sim.op_state==TMmod.INF_REPEAT else str(sim.op_state))
except TimeoutError: pass
except Exception as e: res="tool error: %s"%type(e).__name__
signal.alarm(0)
b2=io.StringIO()
with contextlib.redirect_stdout(b2):
    try: sim.print_self()
    except Exception: pass
out=b2.getvalue()
lv=re.findall(r"Level (\d+) rules: (\d+)",out); nz=re.findall(r"Num Nonzeros: (.*)",out)
size=nz[-1][:90] if nz else "?"
print("stack %-10s block %-3d -> %-18s levels %s  size %s  (%.1fs)\n      start: %s"%(",".join(map(str,stack)),block,res,max([int(a) for a,b in lv]) if lv else 0,re.sub(r"\(_\d+ chars_\)","",size),time.time()-t0,start_tape[:110]))
