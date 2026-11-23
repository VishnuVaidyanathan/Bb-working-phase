/* cls5.c BUDGET PART : Vishnu's changed grammar (23 Nov, afternoon):
     - the even digits make one closed loop of FIVE states A0->B0->C0->D0->E0->A (A0 = 1RB; the others write 0/1, move L/R);
     - the odd halves of the five loop states: exactly one door (any write/move, goes to F), three fillers (write 1, L or R,
       own state), one take (write 0, L or R, own state) - in any arrangement;
     - two states F and G behind the door; of their four wires one is the halt, the other three are free
       (any write, any move, any of the seven states).
   Tables are built only as far as a run from a blank tape needs them.  BUDGET = steps allowed while wires are still open.
   PART = 0..3 picks what B0 does (to split the work), -1 = all.
   A full table is then run on: 20,000 steps (dropped if it halts, or has fewer than 4 or more than 40 runs of 1s) and
   60,000 steps (dropped if it halts, or the runs grew, or the ones did not).  The kept tables are printed.  Thought tool only. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define TW 2001
#define BT 200001
int W[14],M[14],X[14],set[14];
int nfill=3,ntake=1,ndoor=1,nhalt=1,part;
long budget,full=0,halted=0,partial=0,h20=0,shape=0,h60=0,grow=0,kept=0,maxhalt=0,maxones=0;
static unsigned char big[BT];
void name(char*t){t[0]=0;for(int i=0;i<14;i++){if(X[i]<0)strcat(t,"1RZ");else sprintf(t+strlen(t),"%d%c%c",W[i],M[i]>0?'R':'L','A'+X[i]);if(i%2&&i<13)strcat(t,"_");}}
void leaf(unsigned char*tape,long pos,int st,long k){
  full++;long off=BT/2-TW/2;memcpy(big+off,tape,TW);pos+=off;long lo=off,hi=off+TW-1;int end=0;long o20=0;int r20=0;
  for(int stage=0;stage<2&&!end;stage++){long lim=stage?60000:20000;
    for(;k<lim;k++){int i=st*2+big[pos];if(X[i]<0){end=1;break;}big[pos]=W[i];pos+=M[i];st=X[i];if(pos<lo)lo=pos;if(pos>hi)hi=pos;}
    if(end){long o=0;for(long q=lo;q<=hi;q++)o+=big[q];if(k>maxhalt){maxhalt=k;maxones=o;}if(stage)h60++;else h20++;break;}
    long o=0;int r=0;for(long q=lo;q<=hi;q++){o+=big[q];if(big[q]&&!big[q-1])r++;}
    if(!stage){if(r<4||r>40){shape++;end=2;}o20=o;r20=r;}
    else{if(r>r20||o<=o20){grow++;end=2;}else{char t[120];name(t);printf("%s %ld %d\n",t,o,r);kept++;}}
  }
  memset(big+lo-1,0,hi-lo+3);
}
void go(unsigned char*tape,long pos,int st,long k,int nset){
  for(;;){
    if(k>=budget){partial++;return;}
    int i=st*2+tape[pos];
    if(!set[i]){
      unsigned char cp[TW];
      #define TRY(w,m,x) {W[i]=w;M[i]=m;X[i]=x;set[i]=1;memcpy(cp,tape,TW);go(cp,pos,st,k,nset+1);set[i]=0;}
      if(st>=5){for(int w=0;w<2;w++)for(int m=-1;m<2;m+=2)for(int x=0;x<7;x++)TRY(w,m,x)
                if(nhalt)halted++;}
      else if(!(i&1)){if(i==2&&part>=0){TRY(part&1,(part&2)?1:-1,2)}else for(int w=0;w<2;w++)for(int m=-1;m<2;m+=2)TRY(w,m,(st+1)%5)}
      else{
        if(nfill){nfill--;TRY(1,-1,st)TRY(1,1,st)nfill++;}
        if(ntake){ntake--;TRY(0,-1,st)TRY(0,1,st)ntake++;}
        if(ndoor){ndoor--;for(int w=0;w<2;w++)for(int m=-1;m<2;m+=2)TRY(w,m,5)ndoor++;}
      }
      return;
    }
    tape[pos]=W[i];pos+=M[i];st=X[i];k++;
    if(pos<1||pos>TW-2){partial++;return;}
    if(nset==13){int h=-1;for(int j=10;j<14;j++)if(!set[j])h=j;if(h<0){partial++;return;}
      X[h]=-1;W[h]=1;M[h]=1;set[h]=1;leaf(tape,pos,st,k);set[h]=0;return;}
  }
}
int main(int c,char**v){budget=atol(v[1]);part=atoi(v[2]);unsigned char tape[TW];memset(tape,0,TW);
  W[0]=1;M[0]=1;X[0]=1;set[0]=1;go(tape,TW/2,0,0,1);
  fprintf(stderr,"part %d | full tables %ld | halted with a wire still open %ld | still open after the budget %ld\n  of the full tables: halt by 20,000 steps %ld | wrong number of runs %ld | halt by 60,000 %ld | runs grew or ones did not %ld | KEPT %ld\n  latest halt: step %ld with %ld ones\n",part,full,halted,partial,h20,shape,h60,grow,kept,maxhalt,maxones);}
