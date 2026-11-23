/* batch.c STEPS < tables : run each table (one per line, up to 10 states) from a blank tape.
   Prints  HALT steps ones table   or   RUN ones runs table   (runs = number of separate runs of 1s) or OFF table.  Thought tool only. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define TL 20000000
static unsigned char tape[TL];
int main(int c,char**v){long steps=atol(v[1]);char t[200];
  while(scanf("%199s",t)==1){int n=(strlen(t)+1)/7,W[20],M[20],X[20];
    for(int q=0;q<n;q++)for(int b=0;b<2;b++){char*e=t+q*7+b*3;int i=q*2+b;W[i]=e[0]-'0';M[i]=e[1]=='R'?1:-1;X[i]=(e[2]=='Z'||e[2]=='-')?-1:e[2]-'A';}
    long pos=TL/2,lo=pos,hi=pos,k;int st=0,end=0;
    for(k=0;k<steps;k++){int i=st*2+tape[pos];tape[pos]=W[i];pos+=M[i];if(pos<lo)lo=pos;if(pos>hi)hi=pos;if(X[i]<0){end=1;k++;break;}st=X[i];if(pos<3||pos>TL-3){end=2;break;}}
    long o=0,r=0;for(long q=lo;q<=hi;q++){o+=tape[q];if(tape[q]&&(q==lo||!tape[q-1]))r++;}
    if(end==1)printf("HALT %ld %ld %s\n",k,o,t);else if(end==2)printf("OFF 0 0 %s\n",t);else printf("RUN %ld %ld %s\n",o,r,t);
    memset(tape+lo-1,0,hi-lo+3);}
}
