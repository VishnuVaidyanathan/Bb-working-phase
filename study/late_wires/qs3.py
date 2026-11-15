# Quick_Sim on each table; writes: table RESULT levels=N size=...
import subprocess,sys,re,os
QS='/tmp/claude-0/-home-claude/4b1f9c95-7cd8-5462-90c3-009c8e8939ee/scratchpad/tools/busy-beaver/Code/Quick_Sim.py'
inp,out,T=sys.argv[1],sys.argv[2],float(sys.argv[3]); extra=sys.argv[4:]
done=set(l.split()[0] for l in open(out)) if os.path.exists(out) else set()
fo=open(out,'a')
for line in open(inp):
    t=line.split()[-1]
    if t in done: continue
    try: o=subprocess.run(['python3',QS]+extra+[t],capture_output=True,text=True,timeout=T).stdout
    except subprocess.TimeoutExpired as e:
        o=e.stdout or ''
        if isinstance(o,bytes): o=o.decode(errors='replace')
        o+='\nTIMEOUT\n'
    lv=[int(a) for a,b in re.findall(r'Level (\d+) rules: (\d+)',o)]
    nz=re.findall(r'^(?:Num )?Nonzeros:\s+(.*)$',o,re.M)
    size=re.sub(r'\(_\d+ chars_\)','',nz[-1]).split('] (')[0][:90] if nz else '?'
    if 'Turing Machine Halted' in o or 'Undefined transition' in o: r='HALT'
    elif 'proven Infinite' in o: r='INF'
    elif 'TIMEOUT' in o: r='T'
    else: r='OTHER'
    fo.write("%s %s levels=%d size=%s\n"%(t,r,max(lv) if lv else 0,size.replace(' ','_'))); fo.flush()
