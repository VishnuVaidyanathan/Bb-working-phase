// ovf.c : tables from stdin, judged WITHOUT their start on hand-made tapes in the layout of TM 721
// ( head in state D on the blank cell left of the first run; runs of 1s with one empty cell between them ).
// tape 0 = (3 3 3): does a lone counter still become a long row?  -> most runs of 1s seen within 400000 steps, or H step.
// tapes (3 b c), b = 3..10, c = 1..6, 60000 steps each: a string of 48 marks:  . running   e halted early (< 500 steps)   L halted late
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define TL 2000000
static unsigned char tape[TL];
static long lo,hi;
static int w[8][2],m[8][2],n[8][2];
static long run(const int*cf,int nc,long N,long*maxruns,int*res){
  memset(tape+lo-4,0,hi-lo+9);long home=TL/2,p=home+1;
  for(int i=0;i<nc;i++){for(int k=0;k<cf[i];k++)tape[p++]=1;p++;}
  long pos=home,st=3,k;lo=home;hi=p;*res='R';*maxruns=0;
  for(k=0;k<N;k++){int b=tape[pos];int nx=n[st][b];if(nx<0){*res='H';break;}tape[pos]=w[st][b];pos+=m[st][b];st=nx;if(pos<lo)lo=pos;if(pos>hi)hi=pos;if(pos<8||pos>TL-8){*res='X';break;}
    if(maxruns&&k%4000==3999){long r=0,in=0;for(long i=lo;i<=hi;i++){if(tape[i]){if(!in){r++;in=1;}}else in=0;}if(r>*maxruns)*maxruns=r;}}
  return k;}
int main(){char s[200];lo=hi=TL/2;
 while(scanf("%199s",s)==1){
  for(int q=0;q<7;q++)for(int b=0;b<2;b++){char*e=s+q*7+b*3;if(e[2]=='-'||e[2]=='Z'){n[q][b]=-1;w[q][b]=1;m[q][b]=1;}else{w[q][b]=e[0]-'0';m[q][b]=e[1]=='R'?1:-1;n[q][b]=e[2]-'A';}}
  long mr;int res;int c0[3]={3,3,3};long k=run(c0,3,400000,&mr,&res);
  printf("%s %c %ld %ld ",s,res,k,mr);
  for(int b=3;b<=10;b++)for(int c=1;c<=6;c++){int cf[3]={3,b,c};long dm;k=run(cf,3,60000,&dm,&res);putchar(res=='R'?'.':(res=='X'?'x':(k<500?'e':'L')));}
  putchar('\n');}
 return 0;}
