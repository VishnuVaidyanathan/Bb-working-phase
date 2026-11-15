"""Quick_Sim on D1, paused at the boot tape; the whole left side is replaced by a given list.
   usage: python3 from_tape2.py "01:1 11:1 10:4 11:1 10:3 11:1 01:8" [seconds] [trace]
   (the head stays as it is:  (00) E> 10 )"""
import sys,os,re,runpy,time,copy,signal,io,contextlib
QS=os.environ.get("QUICK_SIM_DIR", os.path.expanduser("~/busy-beaver/Code"))   # the Code folder of sligocki/busy-beaver
sys.path.insert(0,QS); os.chdir(QS)
TM="1RB1RD_1LC0RD_0LG1LD_1RA0RE_1LF1LA_0LC1LE_1RZ0LE"
spec=sys.argv[1]; limit=int(sys.argv[2]) if len(sys.argv)>2 else 60; trace=int(sys.argv[3]) if len(sys.argv)>3 else 0
sys.argv=["Quick_Sim.py","-r","--exp-linear-rules","--exp-meta-linear-rules","--no-steps","--manual","--quiet",TM]
with contextlib.redirect_stdout(io.StringIO()):
    g=runpy.run_path(os.path.join(QS,"Quick_Sim.py"),run_name="__main__")
sim=g["sim"]; TMmod=g["Turing_Machine"]
want=re.compile(r"01\^1 11\^1 10\^4 11\^1 10\^3 11\^1 01\^8 ")
for _ in range(200000):
    if want.search(sim.tape.print_with_state(sim.state)): break
    sim.step()
L=sim.tape.tape[0]
proto={}
for x in L:
    nm=x.to_string(False,False).split("^")[0]
    proto.setdefault(nm,x)
new=[L[0]]
for tok in spec.split():
    nm,v=tok.split(":"); y=copy.deepcopy(proto[nm]); y.num=int(v); new.append(y)
L[:]=new
try: sim.prover.past_configs.clear()
except Exception: pass
start=sim.tape.print_with_state(sim.state)
def bye(*a): raise TimeoutError()
signal.signal(signal.SIGALRM,bye); signal.alarm(limit)
t0=time.time(); res="no answer in %d s"%limit; seen=[]
try:
    while sim.op_state==TMmod.RUNNING:
        if trace and len(seen)<trace:
            sim.step(); s=sim.tape.print_with_state(sim.state)
            if not seen or s!=seen[-1]: seen.append(s)
        else: sim.loop_run(1000)
    res="HALT" if sim.op_state in (TMmod.HALT,TMmod.UNDEFINED) else ("runs forever" if sim.op_state==TMmod.INF_REPEAT else str(sim.op_state))
except TimeoutError: pass
except Exception as e: res="tool error: %s %s"%(type(e).__name__,str(e)[:60])
signal.alarm(0)
b2=io.StringIO()
with contextlib.redirect_stdout(b2):
    try: sim.print_self()
    except Exception: pass
out=b2.getvalue()
lv=re.findall(r"Level (\d+) rules: (\d+)",out); nz=re.findall(r"Num Nonzeros: (.*)",out)
size=re.sub(r"\(_\d+ chars_\)","",nz[-1])[:70] if nz else "?"
print("%-46s -> %-14s levels %s  size %s"%(spec,res,max([int(a) for a,b in lv]) if lv else 0,size))
for s in seen: print("      ",s[:150])
