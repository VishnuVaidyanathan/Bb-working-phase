// deepn.c TABLE N : one table on tapes block 3, k empty levels (k = 1..12), stores 4 4.  Prints steps to halt and ones for each k.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define TL 400000000
int main(int c,char**v){char*s=v[1];long N=atol(v[2]);unsigned char*tape=calloc(TL,1);int w[8][2],m[8][2],n[8][2];
  for(int q=0;q<7;q++)for(int b=0;b<2;b++){char*e=s+q*7+b*3;if(e[2]=='-'||e[2]=='Z'){n[q][b]=-1;w[q][b]=1;m[q][b]=1;}else{w[q][b]=e[0]-'0';m[q][b]=e[1]=='R'?1:-1;n[q][b]=e[2]-'A';}}
  long LO=TL/2,HI=TL/2;
  for(int lev=1;lev<=12;lev++){
   memset(tape+LO-8,0,HI-LO+16);long home=TL/2,p=home+1;
   for(int k=0;k<3;k++)tape[p++]=1; p++; p+=lev; for(int k=0;k<4;k++)tape[p++]=1; p++; for(int k=0;k<4;k++)tape[p++]=1;
   long pos=home,st=3,k,lo=home,hi=p;int res='R';
   for(k=0;k<N;k++){int b=tape[pos];int nx=n[st][b];if(nx<0){res='H';break;}tape[pos]=w[st][b];pos+=m[st][b];st=nx;if(pos<lo)lo=pos;if(pos>hi)hi=pos;if(pos<16||pos>TL-16){res='X';break;}}
   long ones=0;for(long i=lo;i<=hi;i++)ones+=tape[i];LO=lo;HI=hi;
   printf("%d empty levels: %c steps %ld ones %ld\n",lev,res,k,ones);fflush(stdout);
   if(res!='H')break;}
  return 0;}
