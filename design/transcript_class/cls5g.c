/* cls5g.c BUDGET PART : Vishnu's grammar of 23 Nov, afternoon, with the gate behind the door:
     - even digits: one closed loop of FIVE states A0->B0->C0->D0->E0->A (A0 = 1RB; the others write 0/1, move L/R);
     - odd halves of the five loop states: exactly one door (any write/move, goes to F), three fillers (write 1, own state),
       one take (write 0, own state), in any arrangement;
     - F is behind the door: one of its wires goes back (to a loop state or to F itself), the other goes on to G;
     - G is the gate behind F: one of its wires is the HALT, the other is free (any write, move, state).
   Tables are built only as far as a run from a blank tape needs them.  Every wire except G's must be reached within BUDGET
   steps; G may be reached at any time, or not at all (then the table is printed with G open: ------).
   PART = 0..3 picks what B0 does (to split the work), -1 = all.
   Checks: at 20,000 steps the tape must have 4 to 40 runs of 1s; at 60,000 steps the runs must not have grown and the ones must have.
   Prints kept tables: table ones runs times-G-was-entered.  Thought tool only. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define BT 140001
int W[14],M[14],X[14],set[14];
int nfill=3,ntake=1,ndoor=1,part;
long budget,partial=0,halts=0,shape=0,grow=0,kept=0,keptopen=0,maxhalt=0,maxones=0;char maxt[120];
unsigned char*buf[16];
void name(char*t){t[0]=0;for(int i=0;i<14;i++){
  if(!set[i]){ if(i>=12&&(set[12]||set[13]))strcat(t,"1RZ"); else strcat(t,"---"); }
  else sprintf(t+strlen(t),"%d%c%c",W[i],M[i]>0?'R':'L','A'+X[i]);
  if(i%2&&i<13)strcat(t,"_");}}
#define RET {memset(tape+lo-1,0,hi-lo+3);return;}
void go(int d,long pos,int st,long k,long lo,long hi,long o20,int r20,long gin){
  unsigned char*tape=buf[d];
  for(;;){
    if(k==budget){for(int j=0;j<12;j++)if(!set[j]){partial++;RET}}
    if(k==20000||k==60000){long o=0;int r=0;for(long q=lo;q<=hi;q++){o+=tape[q];if(tape[q]&&!tape[q-1])r++;}
      if(k==20000){if(r<4||r>40){shape++;RET}o20=o;r20=r;}
      else{if(r>r20||o<=o20){grow++;RET}char t[120];name(t);printf("%s %ld %d %ld\n",t,o,r,gin);kept++;if(!set[12]&&!set[13])keptopen++;RET}}
    int i=st*2+tape[pos];
    if(!set[i]){
      if(i>=12&&(set[12]||set[13])){halts++;if(k>maxhalt){maxhalt=k;maxones=0;for(long q=lo;q<=hi;q++)maxones+=tape[q];name(maxt);}RET}
      unsigned char*cp=buf[d+1];
      #define TRY(w,m,x) {W[i]=w;M[i]=m;X[i]=x;set[i]=1;memcpy(cp+lo-1,tape+lo-1,hi-lo+3);go(d+1,pos,st,k,lo,hi,o20,r20,gin);set[i]=0;}
      if(st==6){for(int w=0;w<2;w++)for(int m=-1;m<2;m+=2)for(int x=0;x<7;x++)TRY(w,m,x)}
      else if(st==5){int other=i^1;
        if(!set[other]||X[other]==6){for(int w=0;w<2;w++)for(int m=-1;m<2;m+=2)for(int x=0;x<6;x++)TRY(w,m,x)}
        if(!set[other]||X[other]!=6){for(int w=0;w<2;w++)for(int m=-1;m<2;m+=2)TRY(w,m,6)}}
      else if(!(i&1)){if(i==2&&part>=0){TRY(part&1,(part&2)?1:-1,2)}else for(int w=0;w<2;w++)for(int m=-1;m<2;m+=2)TRY(w,m,(st+1)%5)}
      else{
        if(nfill){nfill--;TRY(1,-1,st)TRY(1,1,st)nfill++;}
        if(ntake){ntake--;TRY(0,-1,st)TRY(0,1,st)ntake++;}
        if(ndoor){ndoor--;for(int w=0;w<2;w++)for(int m=-1;m<2;m+=2)TRY(w,m,5)ndoor++;}
      }
      RET
    }
    tape[pos]=W[i];pos+=M[i];st=X[i];k++;if(st==6)gin++;
    if(pos<lo)lo=pos;if(pos>hi)hi=pos;
  }
}
int main(int c,char**v){budget=atol(v[1]);part=atoi(v[2]);for(int i=0;i<16;i++)buf[i]=calloc(BT,1);
  W[0]=1;M[0]=1;X[0]=1;set[0]=1;go(0,BT/2,0,0,BT/2,BT/2,0,0,0);
  fprintf(stderr,"part %d | a wire (not G) still open after the budget: %ld | halted: %ld | wrong number of runs at 20,000: %ld | runs grew or ones did not at 60,000: %ld | KEPT %ld (of them G never reached: %ld)\n  latest halt: step %ld with %ld ones  %s\n",part,partial,halts,shape,grow,kept,keptopen,maxhalt,maxones,maxt);}
