/* gate.c STEPS CHECKS < tables : for 7-state tables where G is the gate (state G = the 7th state).
   Runs each table from a blank tape.  Counts how many times G is entered, when it was entered first and last,
   and (as pay.c) how many times a run of 1s got shorter between two checks while the number of runs stayed the same.
   A real rare gate is entered again and again, later and later - not only in the first few steps.
   Prints: G-entries first-G-step last-G-step shrinks ones runs table [HALT|OFF].  Thought tool only. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define TL 8000000
#define MR 64
static unsigned char tape[TL];
int main(int c,char**v){long steps=atol(v[1]);int checks=atoi(v[2]);char t[200];
  while(scanf("%199s",t)==1){int n=(strlen(t)+1)/7,W[20],M[20],X[20];
    for(int q=0;q<n;q++)for(int b=0;b<2;b++){char*e=t+q*7+b*3;int i=q*2+b;W[i]=e[0]-'0';M[i]=e[1]=='R'?1:-1;X[i]=(e[2]=='Z'||e[2]=='-')?-1:e[2]-'A';}
    long pos=TL/2,lo=pos,hi=pos,k=0,g=0,gf=-1,gl=-1;int st=0,end=0,shr=0,pn=-1;long pr[MR],cr[MR];long o=0;int r=0;
    for(int ch=0;ch<checks&&!end;ch++){long lim=steps/checks*(ch+1);
      for(;k<lim;k++){int i=st*2+tape[pos];tape[pos]=W[i];pos+=M[i];if(pos<lo)lo=pos;if(pos>hi)hi=pos;if(X[i]<0){end=1;break;}
        if(X[i]==6&&st!=6){g++;gl=k;if(gf<0)gf=k;}st=X[i];if(pos<3||pos>TL-3){end=2;break;}}
      o=0;r=0;long a=0;for(long q=lo;q<=hi+1;q++){if(q<=hi&&tape[q]){a++;o++;}else if(a){if(r<MR)cr[r]=a;r++;a=0;}}
      if(r==pn&&r<=MR){for(int j=0;j<r;j++)if(cr[j]<pr[j]){shr++;break;}}
      pn=r;if(r<=MR)memcpy(pr,cr,sizeof(long)*r);}
    printf("%ld %ld %ld %d %ld %d %s%s\n",g,gf,gl,shr,o,r,t,end==1?" HALT":end==2?" OFF":"");
    memset(tape+lo-1,0,hi-lo+3);}
}
