"""jeff_stack.py PIECES EVENTS SPEC... : thought experiments on Jeff Ketchersid's champion from a hand-made tape (not a blank-tape run).
   SPEC like 4.2,6.4 = 4 ones, 2 zeros, 6 ones, 4 zeros, then PIECES pieces 1100 and a final 1.  Needs jexp built from jexp.c in this folder.
   Prints the stack of stores at each ticket (each time digit c is read after digit 1)."""
import subprocess,sys
J='1RB0RG_1RC1RB_0RD1RZ_0LE0LD_0LF1LE_1RA1LF_1LC0RB'
def go(spec,m,steps=300000000,ev=6,quiet=False):
    # spec like "4.2,6.4" : 4 ones, 2 zeros, 6 ones, 4 zeros, then m pieces 1100 and a final 1.   tape: 10 [0] ...
    right='0'+''.join('1'*int(a)+'0'*int(b) for a,b in (x.split('.') for x in spec.split(',')))+'1100'*m+'1'
    o=subprocess.run([__file__.rsplit('/',1)[0]+'/jexp',J,'G','10',right,str(steps),str(ev)],capture_output=True,text=True).stdout.strip().split('\n')
    return o
if __name__=="__main__":
    for spec in sys.argv[3:]:
        o=go(spec,int(sys.argv[1]),ev=int(sys.argv[2]))
        print("[%s] + %s pieces"%(spec,sys.argv[1]))
        for l in o: print("     "+" ".join(l.split()[1:]))
