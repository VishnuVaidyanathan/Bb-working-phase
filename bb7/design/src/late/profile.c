// A grammar profile that does not depend on state names.
// Cut the transcript into lines at the least-heavy "once per line" event: here, every time the head turns
// around at the right end (direction changes from right to left). Print the differences between the lengths
// of consecutive lines, as runs:  "+6 x 13" means 13 lines in a row, each 6 longer than the one before.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define TS (1<<24)
static unsigned char t[TS];
int main(int argc,char**argv){ const char*tm=argv[1]; int st=argv[2][0]-'A'; long N=atol(argv[3]); int maxruns=atoi(argv[4]);
  int W[7][2],D[7][2],X[7][2],def[7][2]; memset(def,0,sizeof def);
  for(int s=0;s<7;s++)for(int b=0;b<2;b++){const char*c=tm+s*7+b*3; if(c[0]=='-'||c[2]=='Z')continue; def[s][b]=1; W[s][b]=c[0]-'0'; D[s][b]=c[1]=='R'?1:-1; X[s][b]=c[2]-'A';}
  long pos=TS/2; int lastd=1; long linestart=0, prevlen=-1; long curdiff=1<<30, runlen=0; int printed=0;
  for(long s=0;s<N;s++){ int b=t[pos]; if(!def[st][b]){printf(" HALT@%ld",s);break;}
    int d=D[st][b]; t[pos]=W[st][b]; pos+=d; st=X[st][b];
    if(lastd==1&&d==-1){ long len=s-linestart; linestart=s;
      if(prevlen>=0){ long df=len-prevlen; if(df==curdiff) runlen++; else { if(runlen>=3){ printf(" %+ldx%ld",curdiff,runlen); if(++printed>=maxruns)break; } curdiff=df; runlen=1; } }
      prevlen=len; }
    lastd=d; if(pos<8||pos>TS-8)break; }
  printf("\n"); }
