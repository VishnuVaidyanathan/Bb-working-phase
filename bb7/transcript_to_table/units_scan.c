// for each table: run from blank; at each event "G reads 0" look at the tape right of the head.
// report the first time it is  1^a 0^g (1100)^u 1^z <end>  with u>=3, and the largest u seen.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define TS (1<<22)
static unsigned char tape[TS];
int main(int c,char**v){ long cap=atol(v[1]); char line[256];
 while(fgets(line,256,stdin)){ char*tm=strrchr(line,' '); tm=tm?tm+1:line; tm[strcspn(tm,"\n")]=0;
  int W[7][2],M[7][2],N[7][2]; for(int s=0;s<7;s++)for(int r=0;r<2;r++){const char*p=tm+s*7+r*3; if(p[0]=='-'||p[2]=='Z'){N[s][r]=-1;continue;} W[s][r]=p[0]-'0';M[s][r]=p[1]=='R'?1:-1;N[s][r]=p[2]-'A';}
  memset(tape,0,TS); long p=TS/2,lo=p,hi=p; int s=0; long t; int best=0; long ba=0,bg=0,bz=0,bt=0; int nev=0; int halted=0;
  for(t=0;t<cap;t++){ int r=tape[p];
   if(s==6&&r==0&&t>0){ nev++; while(hi>p&&!tape[hi])hi--; long i=p+1; long a=0; while(i<=hi&&tape[i]){a++;i++;} long g=0; while(i<=hi&&!tape[i]){g++;i++;}
     int u=0; while(i+3<=hi+1&&tape[i]&&tape[i+1]&&!tape[i+2]&&!tape[i+3]){u++;i+=4;} long z=0; while(i<=hi&&tape[i]){z++;i++;}
     if(i>hi&&u>best){best=u;ba=a;bg=g;bz=z;bt=t;} }
   if(N[s][r]<0){halted=1;break;}
   tape[p]=W[s][r]; p+=M[s][r]; s=N[s][r]; if(p<lo)lo=p; if(p>hi)hi=p; if(p<8||p>TS-8)break; }
  printf("%s u=%d a=%ld g=%ld z=%ld t=%ld events=%d %s\n",tm,best,ba,bg,bz,bt,nev,halted?"HALT":""); fflush(stdout); } }
