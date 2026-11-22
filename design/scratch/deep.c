// deep.c N : tables from stdin on hand-made tapes of OUR layout (head in state D on the blank cell left of the block; solid runs,
// one empty cell between stores, one MORE empty cell for every empty level).  Tapes: block 3, then 1, 2, 3, 4 empty levels, then 4 4.
// Also (3 7) and (3 6 6) as checks of the number test.  Prints per tape: H steps ones | R ones (still running after N) | X (off the tape)
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define TL 40000000
static unsigned char *tape;
static const int CF[][10]={{3,7,-1},{3,6,6,-1},{3,0,4,4,-1},{3,0,0,4,4,-1},{3,0,0,0,4,4,-1},{3,0,0,0,0,4,4,-1},{-1}};
int main(int c,char**v){long N=atol(v[1]);char s[200];tape=calloc(TL,1);long LO=TL/2,HI=TL/2;
 while(scanf("%199s",s)==1){int w[8][2],m[8][2],n[8][2];
  for(int q=0;q<7;q++)for(int b=0;b<2;b++){char*e=s+q*7+b*3;if(e[2]=='-'||e[2]=='Z'){n[q][b]=-1;w[q][b]=1;m[q][b]=1;}else{w[q][b]=e[0]-'0';m[q][b]=e[1]=='R'?1:-1;n[q][b]=e[2]-'A';}}
  printf("%s",s);
  for(int t=0;CF[t][0]>=0;t++){
   memset(tape+LO-8,0,HI-LO+16);long home=TL/2,p=home+1;
   for(int i=0;CF[t][i]>=0;i++){for(int k=0;k<CF[t][i];k++)tape[p++]=1;p++;}
   long pos=home,st=3,k,lo=home,hi=p;int res='R';
   for(k=0;k<N;k++){int b=tape[pos];int nx=n[st][b];if(nx<0){res='H';break;}tape[pos]=w[st][b];pos+=m[st][b];st=nx;if(pos<lo)lo=pos;if(pos>hi)hi=pos;if(pos<16||pos>TL-16){res='X';break;}}
   long ones=0;for(long i=lo;i<=hi;i++)ones+=tape[i];LO=lo;HI=hi;
   if(res=='H')printf(" | H %ld %ld",k,ones);else printf(" | %c %ld",res,ones);
  }
  printf("\n");fflush(stdout);}
 return 0;}
