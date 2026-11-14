# run Ligocki's Quick_Sim on each table (file given), skip tables already in the output file.
import subprocess,sys,re,os
QS='/tmp/claude-0/-home-claude/4b1f9c95-7cd8-5462-90c3-009c8e8939ee/scratchpad/tools/busy-beaver/Code/Quick_Sim.py'
inp,out,T=sys.argv[1],sys.argv[2],float(sys.argv[3]); extra=sys.argv[4:]
done=set(l.split()[0] for l in open(out)) if os.path.exists(out) else set()
fo=open(out,'a')
for line in open(inp):
    t=line.split()[-1]
    if t in done: continue
    tm=t.replace('---','1RZ')
    try:
        o=subprocess.run(['python3',QS]+extra+[tm],capture_output=True,text=True,timeout=T).stdout
    except subprocess.TimeoutExpired as e:
        o=e.stdout or ''
        if isinstance(o,bytes): o=o.decode(errors='replace')
        o+='\nTIMEOUT\n'
    rp=re.findall(r'Rules proven: (\d+)',o); st=re.findall(r'^Total:\s+(.*?)\s{3,}',o,re.M)
    if 'Turing Machine Halted' in o:
        s=re.findall(r'^Steps:\s+(.*)$',o,re.M); n=re.findall(r'^Nonzeros:\s+(.*)$',o,re.M)
        r='HALT steps '+(s[-1][:80] if s else '?')+' ones '+(n[-1][:80] if n else '?')
    elif 'proven Infinite' in o:
        s=re.findall(r'^Reason: (\S+)',o,re.M); r='INF '+(s[-1] if s else '?')
    elif 'TIMEOUT' in o: r='T'
    else: r='OTHER '+' '.join(o.strip().split('\n')[-2:])[:100]
    fo.write(f"{t} {r} | rules {rp[-1] if rp else '-'} total {st[-1][:40] if st else '-'}\n"); fo.flush()
