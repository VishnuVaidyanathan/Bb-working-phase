// fam.c N : tables from stdin, each run from a blank tape for N steps.  Every 100000 steps (and at the end) the tape is read as runs of 1s.
// prints: table  H|R  steps  ones  maxruns (most runs of 1s seen at a sample)  maxrun (longest run seen)  extent
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define TL 8000000
static unsigned char tape[TL];
int main(int c,char**v){long N=atol(v[1]);char s[200];
 while(scanf("%199s",s)==1){int w[8][2],m[8][2],n[8][2];int NQ=(strlen(s)+1)/7;
  for(int q=0;q<NQ;q++)for(int b=0;b<2;b++){char*e=s+q*7+b*3;if(e[2]=='-'||e[2]=='Z'){n[q][b]=-1;w[q][b]=1;m[q][b]=1;}else{w[q][b]=e[0]-'0';m[q][b]=e[1]=='R'?1:-1;n[q][b]=e[2]-'A';}}
  long pos=TL/2,lo=pos,hi=pos,st=0,k;int res='R';long maxruns=0,maxrun=0;
  for(k=0;k<N;k++){int b=tape[pos];int nx=n[st][b];if(nx<0){res='H';break;}tape[pos]=w[st][b];pos+=m[st][b];st=nx;if(pos<lo)lo=pos;if(pos>hi)hi=pos;if(pos<8||pos>TL-8){res='X';break;}
   if(k%100000==99999){long runs=0,run=0;for(long i=lo;i<=hi;i++){if(tape[i]){run++;}else{if(run){runs++;if(run>maxrun)maxrun=run;}run=0;}}if(run){runs++;if(run>maxrun)maxrun=run;}if(runs>maxruns)maxruns=runs;}}
  long ones=0,runs=0,run=0;for(long i=lo;i<=hi;i++){ones+=tape[i];if(tape[i]){run++;}else{if(run){runs++;if(run>maxrun)maxrun=run;}run=0;}}if(run){runs++;if(run>maxrun)maxrun=run;}if(runs>maxruns)maxruns=runs;
  printf("%s %c %ld %ld %ld %ld %ld\n",s,res,k,ones,maxruns,maxrun,hi-lo);
  memset(tape+lo-2,0,hi-lo+5);}
 return 0;}
