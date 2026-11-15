import re,os,sys,json
from profile import profile
names={"J":"Jeff Ketchersid (claimed champion)","J2":"Jeff Ketchersid (second table)","P":"Pavel Kropitz","D1":"Andrew Ducharme","Q1":"@prurq","D2":"Andrew Ducharme","D3":"Andrew Ducharme","D4":"Andrew Ducharme","D5":"Andrew Ducharme","D6":"Andrew Ducharme","D7":"Andrew Ducharme","D8":"Andrew Ducharme","D9":"Andrew Ducharme","T286":"Terry Ligocki","T246":"found in @Iijil's range","T140":"found in @stokastic's range","T93":"found in the Iijil / Terry Ligocki range","T46":"Terry Ligocki","T35":"listed May 2025","T22":"Shawn Ligocki","W5":"Kropitz, Michel, Wythagoras","S5":"6-state, from Shawn Ligocki's collection","T15":"Pavel Kropitz (6 states)","S6":"BB(6) champion (rules by mxdys)"}
rows=[]
for line in open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "machines.txt")):
    n,tm=line.split();f="qs_%s.out"%n
    lv="";res="";size="";base="";mod=""
    if os.path.exists(f):
        o=open(f).read()
        L=re.findall(r'Level (\d+) rules: (\d+)',o)
        # keep the last block of level lines
        last={}
        for a,b in L: last[int(a)]=int(b)
        lv=str(max(last)) if last else "0"
        res="halts" if "Turing Machine Halted" in o or "Undefined transition" in o else ("runs forever" if "Infinite" in o else "no answer in 150 s")
        m=re.findall(r'^Nonzeros:\s+(.*)$',o,re.M)
        if m:
            z=m[-1]
            a=re.match(r'\[([^,\]]*)',z)
            size=a.group(1).strip() if a else z[:40]
            b=re.findall(r'(\d+)\^\(',z); base=",".join(sorted(set(b),key=b.count,reverse=True)[:2])
            d=re.findall(r'\)/(\d+)\)',z); mod=",".join(sorted(set(d),key=d.count,reverse=True)[:2])
    pr=profile(tm,800000)
    pic=pr['pic']
    store=[]
    if re.search(r'\(10\)\^\d{2,}',pic): store.append("stripes (10)^m")
    for mot in ("1100","1110","110","100","1101","1000"):
        if re.search(r'\(%s\)\^\d{2,}'%mot,pic): store.append("units %s"%mot)
    if re.search(r'1\^\d{3,}',pic): store.append("solid block")
    if re.search(r'0\^\d{3,}',pic) or re.search(r'10\^\d{2,}',pic): store.append("gap of zeros")
    rows.append(dict(n=n,tm=tm,who=names.get(n,""),levels=lv,res=res,size=size,base=base,mod=mod,allby=pr['allby'],single=",".join(pr['single']) or "-",pairs=",".join(pr['pairs']) or "-",store="; ".join(store) or "?",pic=pic[:110]))
json.dump(rows,open("rows.json","w"),indent=1)
for r in rows: print("%-5s lv %-2s %-18s base %-4s div %-5s all@%-5d fill %-6s pairs %-9s | %s | %s"%(r['n'],r['levels'],r['res'],r['base'],r['mod'],r['allby'],r['single'],r['pairs'],r['store'],r['size'][:60]))
