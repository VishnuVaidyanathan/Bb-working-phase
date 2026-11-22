// tapes.c N : read tables from stdin; run each on hand-made tapes "block, stores" (A at home on the 0 left of the block) and from a blank tape.
// prints per tape: H(steps,ones,payments) if it stops on the halt wire, R(ones,payments) if still running after N steps, X if it leaves the tape.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define TL 60000000
static unsigned char *tape;
static const int CF[][8]={{3,2,4,2,-1},{3,2,4,4,-1},{3,2,4,6,-1},{3,2,4,8,-1},{3,2,2,2,2,-1},{-1}};
int main(int c,char**v){long N=atol(v[1]);char s[200];tape=malloc(TL);
 while(scanf("%199s",s)==1){int w[8][2],m[8][2],n[8][2];int NQ=(strlen(s)+1)/7;
  for(int q=0;q<NQ;q++)for(int b=0;b<2;b++){char*e=s+q*7+b*3;if(e[2]=='-'||e[2]=='Z'){n[q][b]=-1;w[q][b]=1;m[q][b]=1;}else{w[q][b]=e[0]-'0';m[q][b]=e[1]=='R'?1:-1;n[q][b]=e[2]-'A';}}
  printf("%s",s);
  for(int t=0;t<6;t++){
   memset(tape,0,TL);long home=TL/2,p=home+1;
   if(CF[t][0]>=0){for(int i=0;CF[t][i]>=0;i++){for(int k=0;k<CF[t][i];k++)tape[p++]=1;p++;}}
   long pos=home,st=0,k,pay=0;int res='R';
   for(k=0;k<N;k++){int b=tape[pos];if(st==2&&b==0)pay++;int nx=n[st][b];if(nx<0){res='H';break;}tape[pos]=w[st][b];pos+=m[st][b];st=nx;if(pos<8||pos>TL-8){res='X';break;}}
   long ones=0;for(long i=0;i<TL;i++)ones+=tape[i];
   if(res=='H')printf(" | H %ld %ld %ld",k,ones,pay);else printf(" | %c %ld %ld",res,ones,pay);
  }
  printf("\n");fflush(stdout);}
 return 0;}
