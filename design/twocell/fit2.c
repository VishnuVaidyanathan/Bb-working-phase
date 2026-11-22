// fit.c : tables from stdin.  Each is put on hand-made tapes in the two-empty-cell layout ( 1 [A]0 block 00 store 00 store ... ,
// an empty level = two more empty cells ) and run to its NEXT home visit (state A reading 0).  Prints what the tape then reads as:
// left-ones : block ; stores      (or H = halted first, N = no home visit within the step limit)
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define TL 60000
static unsigned char tape[TL];static long LO=TL/2,HI=TL/2;
static const int CF[][8]={{7,0,4,3,-1},{6,0,0,4,3,-1},{9,0,0,0,4,3,-1},{7,0,5,3,-1},{-1}};
int main(int c,char**v){long N=atol(v[1]);char s[200];
 while(scanf("%199s",s)==1){int w[8][2],m[8][2],n[8][2];int NQ=(strlen(s)+1)/7;
  for(int q=0;q<NQ;q++)for(int b=0;b<2;b++){char*e=s+q*7+b*3;if(e[2]=='-'||e[2]=='Z'){n[q][b]=-1;w[q][b]=1;m[q][b]=1;}else{w[q][b]=e[0]-'0';m[q][b]=e[1]=='R'?1:-1;n[q][b]=e[2]-'A';}}
  printf("%s",s);
  for(int t=0;CF[t][0]>=0;t++){
   if(t==0)memset(tape,0,TL);else memset(tape+LO-8,0,HI-LO+16);long home=TL/2,p=home+1;tape[home-1]=1;
   for(int k=0;k<CF[t][0];k++)tape[p++]=1;
   for(int i=1;CF[t][i]>=0;i++){p+=2;for(int k=0;k<CF[t][i];k++)tape[p++]=1;}
   long pos=home,st=0,k,lo=home-1,hi=p;int res='N';
   for(k=0;k<N;k++){int b=tape[pos];if(k>0&&st==0&&b==0&&tape[pos-1]==1&&!tape[pos-2]&&!tape[pos-3]&&!tape[pos-4]&&!tape[pos-5]){long l=0;for(long i=lo;i<pos;i++)l+=tape[i];if(l==1){res='A';break;}}int nx=n[st][b];if(nx<0){res='H';break;}tape[pos]=w[st][b];pos+=m[st][b];st=nx;if(pos<lo)lo=pos;if(pos>hi)hi=pos;if(pos<8||pos>TL-8){res='X';break;}}
   LO=lo;HI=hi;if(res!='A'){printf(" | %c",res);continue;}
   long left=0;for(long i=lo;i<pos;i++)left+=tape[i];
   printf(" | %ld:",left);
   long q=pos+1;int first=1;
   while(q<=hi+1){long a=0;while(q<=hi+1&&tape[q]){a++;q++;}long z=0;while(q<=hi+1&&!tape[q]){z++;q++;}
     if(first){printf("%ld;",a);first=0;}else printf(" %ld",a);
     if(q>hi+1)break;
     if(z%2||z<2){printf(" ?gap%ld",z);} else for(long e=0;e<(z-2)/2;e++)printf(" 0");}
  }
  printf("\n");}
 return 0;}
