#include <stdio.h>
#include <stdlib.h>
typedef struct{int s;long n;}Run;
#define M 1000000
static Run L[M],R[M];int nl=0,nr=0;
static void push(Run*S,int*n,int s,long c){if(c==0)return;if(*n&&S[*n-1].s==s)S[*n-1].n+=c;else{S[*n].s=s;S[*n].n=c;(*n)++;}}
static int pop1(Run*S,int*n){if(!*n)return 0;int s=S[*n-1].s;if(--S[*n-1].n==0)(*n)--;return s;}
int main(int ac,char**av){const char*t="1RB0RG_1RC1RB_0RD1RZ_0LE0LD_0LF1LE_1RA1LF_1LC0RB";long lim=atol(av[1]);
 int st=0;long kept=0,zeros=0;double steps=0;
 while(kept<lim){int v=nr?R[nr-1].s:0;const char*e=t+st*7+v*3;int w=e[0]-'0',right=e[1]=='R';int d=st*2+v;
  if(e[2]=='Z'){printf("HALT kept %ld steps %.6g\n",kept,steps);return 0;}
  int ns=e[2]-'A';
  if(ns==st){ long c;
    if(right){ if(nr){c=R[nr-1].n;nr--;}else{printf("runs away\n");return 0;} push(L,&nl,w,c);}
    else{ pop1(R,&nr);c=1; if(nl&&L[nl-1].s==v){c+=L[nl-1].n;nl--;} push(R,&nr,w,c); int x=pop1(L,&nl);push(R,&nr,x,1);}
    steps+=c;
  } else { kept++;steps+=1;
    if(d==0)zeros++;
    if(d==1||d==12||d==13){printf("%ld%c ",zeros,"0123456789abcd"[d]);zeros=0;}
    pop1(R,&nr);
    if(right)push(L,&nl,w,1); else{push(R,&nr,w,1);int x=pop1(L,&nl);push(R,&nr,x,1);}
  }
  st=ns;}
 printf("\nkept %ld steps %.6g rounds since last %ld runs %d %d\n",kept,steps,zeros,nl,nr);}
