#include <stdio.h>
#include <stdlib.h>
#include <string.h>
// direct.c: read tables from stdin, run each from a blank tape for N steps; print: table, HALT steps ones | RUN extent
#define TL 40000000
static unsigned char *tape;
int main(int c,char**v){long N=atol(v[1]);char s[200];tape=malloc(TL);
 while(scanf("%199s",s)==1){int w[7][2],m[7][2],n[7][2];
  for(int q=0;q<7;q++)for(int b=0;b<2;b++){char*e=s+q*7+b*3;if(e[2]=='-'||e[2]=='Z'){n[q][b]=-1;w[q][b]=1;m[q][b]=1;}else{w[q][b]=e[0]-'0';m[q][b]=e[1]=='R'?1:-1;n[q][b]=e[2]-'A';}}
  memset(tape,0,TL);long pos=TL/2,lo=pos,hi=pos,st=0,t;int halt=0;
  for(t=0;t<N;t++){int b=tape[pos];int nx=n[st][b];if(nx<0){halt=1;break;}tape[pos]=w[st][b];pos+=m[st][b];st=nx;if(pos<lo)lo=pos;if(pos>hi)hi=pos;if(pos<8||pos>TL-8)break;}
  long ones=0;for(long i=lo;i<=hi;i++)ones+=tape[i];
  if(halt)printf("%s HALT %ld %ld\n",s,t+1,ones);else printf("%s RUN %ld %ld\n",s,hi-lo,ones);}
 return 0;}
