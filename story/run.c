/* run.c TABLE [maxsteps] : run a table from a blank tape; an undefined entry (---) or Z halts. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define W 40000000
static char tape[W];
int main(int ac,char**av){char*t=av[1];long max=ac>2?atol(av[2]):20000000000L;int tr[8][2],n=(strlen(t)+1)/7;
  for(int s=0;s<n;s++)for(int b=0;b<2;b++){char*e=t+s*7+b*3;tr[s][b]=(e[2]=='-'||e[2]=='Z')?-1:(e[0]-'0')|((e[1]=='R')<<1)|((e[2]-'A')<<2);}
  long p=W/2,st=0,lo=p,hi=p;int s=0;
  for(;st<max;){int e=tr[s][(int)tape[p]];if(e<0){long ones=0;for(long i=lo;i<=hi;i++)ones+=tape[i];printf("%s HALT steps %ld ones %ld (state %c reads %d)\n",t,st+1,ones+(t[s*7+tape[p]*3+2]=='Z'),'A'+s,tape[p]);return 0;}
    tape[p]=e&1;p+=(e&2)?1:-1;s=e>>2;st++;if(p<lo)lo=p;if(p>hi)hi=p;if(p<2||p>W-2){printf("%s OFF TAPE at %ld\n",t,st);return 0;}}
  long ones=0;for(long i=lo;i<=hi;i++)ones+=tape[i];printf("%s no halt in %ld steps, ones %ld\n",t,max,ones);return 0;}
