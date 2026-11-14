// run each table from a blank tape up to CAP steps. prints "H steps ones table", "R width table" or "X table" (tape too wide).
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define TS (1<<24)
static unsigned char t[TS];
int main(int argc,char**argv){ long CAP=atol(argv[1]); char line[256]; int W[8][2],D[8][2],X[8][2],def[8][2];
  while(fgets(line,256,stdin)){ char*tm=strrchr(line,' '); tm=tm?tm+1:line; tm[strcspn(tm,"\n")]=0; int NS=(strlen(tm)+1)/7; memset(def,0,sizeof def);
    for(int s=0;s<NS;s++)for(int b=0;b<2;b++){const char*c=tm+s*7+b*3; if(c[0]=='-'||c[2]=='Z')continue; def[s][b]=1; W[s][b]=c[0]-'0'; D[s][b]=c[1]=='R'?1:-1; X[s][b]=c[2]-'A';}
    int pos=TS/2,st=0,lo=pos,hi=pos; long s; int halt=0,wide=0;
    for(s=0;s<CAP;s++){ int b=t[pos]; if(!def[st][b]){halt=1;break;} t[pos]=W[st][b]; pos+=D[st][b]; st=X[st][b];
      if(pos<lo){lo=pos; if(pos<4){wide=1;break;}} else if(pos>hi){hi=pos; if(pos>TS-4){wide=1;break;}} }
    long ones=0; for(int i=lo;i<=hi;i++)ones+=t[i]; memset(t+lo-1,0,hi-lo+3);
    if(halt) printf("H %ld %ld %s\n",s+1,ones,tm); else if(wide) printf("X %s\n",tm); else printf("R %d %s\n",hi-lo,tm); fflush(stdout); } }
