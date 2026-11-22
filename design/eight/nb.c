/* nb.c TABLE STEPS : every table within two wire changes of an 8-state TABLE, each from a blank tape for STEPS steps.
   Prints: tables that halt after step 1000, and tables still running whose tape has 3 or more runs of 1s and 200 or more ones.
   Search inside a hand-made frame (our 8-state engine without its start).  Thought tool only. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define N 8
#define TL 4100000
static unsigned char tape[TL];
int W[16],Mv[16],Nx[16];
long halts_early=0,halts_late=0,off=0,runs_big=0,runs_other=0,total=0;
void show(char*b){for(int i=0;i<16;i++){if(Nx[i]<0)sprintf(b+strlen(b),"1RZ");else sprintf(b+strlen(b),"%d%c%c",W[i],Mv[i]>0?'R':'L','A'+Nx[i]);if(i%2&&i<15)strcat(b,"_");}}
void run(long steps){
  total++;long lo=TL/2,hi=TL/2,pos=TL/2;int st=0;long k;
  for(k=0;k<steps;k++){int i=st*2+tape[pos];if(Nx[i]<0)break;tape[pos]=W[i];pos+=Mv[i];st=Nx[i];if(pos<lo)lo=pos;if(pos>hi)hi=pos;if(pos<2||pos>TL-2)break;}
  char b[200]="";
  if(pos<2||pos>TL-2)off++;
  else if(k<steps){ if(k<1000)halts_early++; else{halts_late++;long o=0;for(long q=lo;q<=hi;q++)o+=tape[q];show(b);printf("HALT %ld ones %ld %s\n",k,o,b);} }
  else{long o=0,r=0;for(long q=lo;q<=hi;q++){o+=tape[q];if(tape[q]&&!tape[q-1])r++;}
    if(r>=3&&o>=200){runs_big++;show(b);printf("RUN ones %ld runs %ld %s\n",o,r,b);}else runs_other++;}
  memset(tape+lo-1,0,hi-lo+3);
}
int main(int c,char**v){
  char*t=v[1];long steps=atol(v[2]);int hw=-1;
  for(int q=0;q<N;q++)for(int b=0;b<2;b++){char*e=t+q*7+b*3;int i=q*2+b;if(e[2]=='Z'||e[2]=='-'){Nx[i]=-1;hw=i;}else{W[i]=e[0]-'0';Mv[i]=e[1]=='R'?1:-1;Nx[i]=e[2]-'A';}}
  int w0[16],m0[16],n0[16];memcpy(w0,W,sizeof W);memcpy(m0,Mv,sizeof Mv);memcpy(n0,Nx,sizeof Nx);
  for(int i=0;i<16;i++){ if(i==hw)continue;
    for(int a=0;a<32;a++){W[i]=a&1;Mv[i]=(a&2)?1:-1;Nx[i]=a>>2;
      if(W[i]==w0[i]&&Mv[i]==m0[i]&&Nx[i]==n0[i]){ if(i==0)run(steps); continue;}
      run(steps);
      for(int j=i+1;j<16;j++){ if(j==hw)continue;
        for(int d=0;d<32;d++){W[j]=d&1;Mv[j]=(d&2)?1:-1;Nx[j]=d>>2;if(W[j]==w0[j]&&Mv[j]==m0[j]&&Nx[j]==n0[j])continue;run(steps);}
        W[j]=w0[j];Mv[j]=m0[j];Nx[j]=n0[j];}
    }
    W[i]=w0[i];Mv[i]=m0[i];Nx[i]=n0[i];}
  fprintf(stderr,"total %ld | halt before 1000: %ld | halt later: %ld | off tape: %ld | running, 3+ runs and 200+ ones: %ld | running, other: %ld\n",total,halts_early,halts_late,off,runs_big,runs_other);
}
