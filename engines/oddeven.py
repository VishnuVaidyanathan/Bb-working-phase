"""oddeven.py : the odd/even algebra of the grammar (round +3, pay 2, land at the deepest empty level, fresh stores of 2), as a tool.
   For new block B0 and added AL:  a payment turns block w into B0 + 3*(w + AL - 2g), which is odd/even like w + B0 + AL;
   the landed block w + AL - 2g is odd/even like w + AL; after a deep payment the block restarts from B0 (+6 for a fresh store).
   So after the first deep payment the block is odd/even like B0, and:
     B0 + AL even  ->  every landed block is even: no payer is ever left with 1, the row lives; its end block is odd/even like B0
                       (B0 odd: HALT at the row end;  B0 even: a new row, and so on for ever)
     B0 + AL odd   ->  the block flips at every payment, landed blocks are odd every other time: the row dies on the base halt
   This file prints that verdict for each choice and, with exact numbers (bench.py), what short START rows do: a start row
   (block r even, n stores of 2 and a 1) that ends on an even block w hands over to one full row of w/2 stores."""
import bench as B
def verdict(B0,AL):
    if (B0+AL)%2: return "rows die (base halt)"
    return "full row lives, ends odd: HALT" if B0%2 else "full row lives, ends even: rows for ever"
if __name__=="__main__":
    for B0 in (1,3,5):
        for AL in (1,3,5,7,9,11):
            best=[]
            for r in (2,4,6,8):
                for n in (1,2,3):
                    res=B.run_row(r,[2]*n+[1],B0,AL,tmax=3)
                    if res[0]=="end" and res[1]%2==0: best.append((res[1],r,n))
            best.sort(reverse=True)
            s="; ".join("start (%d; %s 1) ends on %s -> full row of %s stores"%(r," ".join(["2"]*n),B.short(w),B.short(w//2)) for w,r,n in best[:3])
            print("new block %d, added %2d | %s | %s"%(B0,AL,verdict(B0,AL),s or "no short start row ends even"))
