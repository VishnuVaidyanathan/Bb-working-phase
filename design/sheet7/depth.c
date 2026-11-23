/* depth.c CAP [BASE=4] : frame around the round+payment transcript (compile/round_transcript.md).
   Fixed: A0 1RB, A1 1LA, B0 1RC, B1 1RB, C1 0RD, D0 halt, D1 0LE, G1 1LG, E1 unused (stop).
   Open:  E0 = 1L?, F1 = 1L?, and C0, F0, G0 fully (write, move, state).   49 * 28^3 = 1,075,648 tables.
   Each table runs on hand tapes (3 2 2 e), e = BASE, BASE+2, BASE+4 (head on the empty cell left of the block, state A), CAP steps.
   Depth shows as: the run gets enormously longer with e.  Prints tables where e=4 stops, and e=6 takes 30 times longer or more
   (or passes CAP).  Thought tool only. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define TL 3000000
static unsigned char tape[TL];
int W[14],M[14],X[14];
long run(int e,long cap){
  long p=TL/2,lo=p,hi;int cfg[4]={3,2,2,e};long q=p+1;
  for(int i=0;i<4;i++){for(int j=0;j<cfg[i];j++)tape[q++]=1;q++;}
  hi=q;int st=0;long k;
  for(k=0;k<cap;k++){int i=st*2+tape[p];if(X[i]<0)break;tape[p]=W[i];p+=M[i];st=X[i];if(p<lo)lo=p;if(p>hi)hi=p;if(p<2||p>TL-2){k=cap;break;}}
  memset(tape+lo-1,0,hi-lo+3);return k;}
void set(int i,int a){W[i]=a&1;M[i]=(a&2)?1:-1;X[i]=a>>2;}
int main(int c,char**v){long cap=atol(v[1]);int base=c>2?atoi(v[2]):4;long n=0,stop4=0,flat=0,hit=0;
  /* A0 A1 B0 B1 C0 C1 D0 D1 E0 E1 F0 F1 G0 G1 */
  W[0]=1;M[0]=1;X[0]=1; W[1]=1;M[1]=-1;X[1]=0; W[2]=1;M[2]=1;X[2]=2; W[3]=1;M[3]=1;X[3]=1;
  W[5]=0;M[5]=1;X[5]=3; X[6]=-1; W[7]=0;M[7]=-1;X[7]=4; X[9]=-1; W[13]=1;M[13]=-1;X[13]=6;
  for(int e0=0;e0<7;e0++)for(int f1=0;f1<7;f1++){W[8]=1;M[8]=-1;X[8]=e0;W[11]=1;M[11]=-1;X[11]=f1;
   for(int a=0;a<28;a++)for(int b=0;b<28;b++)for(int d=0;d<28;d++){set(4,a);set(10,b);set(12,d);n++;
    long s4=run(base,cap);if(s4>=cap)continue;stop4++;
    long s6=run(base+2,cap);
    if(s6<30*s4){flat++;continue;}
    long s8=run(base+4,cap);hit++;
    char t[120]="";for(int i=0;i<14;i++){if(X[i]<0)strcat(t,i==6?"1RZ":"---");else sprintf(t+strlen(t),"%d%c%c",W[i],M[i]>0?'R':'L','A'+X[i]);if(i%2&&i<13)strcat(t,"_");}
    printf("%ld %ld %ld %s\n",s4,s6,s8,t);}}
  fprintf(stderr,"tables %ld | stop on e=4: %ld | of those, e=6 less than 30 times longer: %ld | kept: %ld\n",n,stop4,flat,hit);}
