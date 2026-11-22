/* show.c TABLE STEPS : run a table (any number of states up to 10) from a blank tape and print the tape as run lengths
   (a run of 1s; each _ is one more empty cell after it), runs of equal neighbours folded as  n x k.  Thought tool only. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define TL 80000000
static unsigned char tape[TL];
int main(int c,char**v){char*t=v[1];long steps=atol(v[2]);int n=(strlen(t)+1)/7,W[20],M[20],X[20];
  for(int q=0;q<n;q++)for(int b=0;b<2;b++){char*e=t+q*7+b*3;int i=q*2+b;if(e[2]=='Z'||e[2]=='-')X[i]=-1;else{W[i]=e[0]-'0';M[i]=e[1]=='R'?1:-1;X[i]=e[2]-'A';}}
  long pos=TL/2,lo=pos,hi=pos,k;int st=0;
  for(k=0;k<steps;k++){int i=st*2+tape[pos];if(X[i]<0)break;tape[pos]=W[i];pos+=M[i];st=X[i];if(pos<lo)lo=pos;if(pos>hi)hi=pos;if(pos<2||pos>TL-2)break;}
  long o=0;for(long q=lo;q<=hi;q++)o+=tape[q];
  printf("%s %s ones %ld |",t,k<steps?(pos<2||pos>TL-2?"OFF":"HALT"):"run",o);
  long q=lo,pa=-1,pz=-1,rep=0;int out=0;
  while(q<=hi+1&&out<40){long a=0,z=0;while(q<=hi&&tape[q]){a++;q++;}while(q<=hi&&!tape[q]){z++;q++;}
    int end=(q>hi);
    if(a==pa&&z==pz&&!end)rep++;else{if(pa>0){printf(" %ld",pa);for(long j=1;j<pz;j++)putchar('_');if(rep>1)printf("x%ld",rep);out++;}pa=a;pz=z;rep=1;}
    if(end){if(a>0){printf(" %ld",a);}break;}}
  printf("\n");}
