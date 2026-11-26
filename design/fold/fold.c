// fold LIMIT < tables : run each table with every drag taken as one jump; report growth of gaps between firings of each digit
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
typedef struct{int s;long n;}Run;
#define M 200000
static Run L[M],R[M];int nl,nr;
static void push(Run*S,int*n,int s,long c){if(c==0)return;if(*n&&S[*n-1].s==s)S[*n-1].n+=c;else{S[*n].s=s;S[*n].n=c;(*n)++;}}
static int pop1(Run*S,int*n){if(!*n)return 0;int s=S[*n-1].s;if(--S[*n-1].n==0)(*n)--;return s;}
#define H 12
int main(int ac,char**av){long lim=atol(av[1]);char t[128];
 while(scanf("%127s",t)==1){nl=nr=0;int st=0;long kept=0;double steps=0;const char*res="END";
  long cnt[14]={0},last[14][H];memset(last,0,sizeof last);
  while(kept<lim){int v=nr?R[nr-1].s:0;const char*e=t+st*7+v*3;int w=e[0]-'0',right=e[1]=='R';int d=st*2+v;
   if(e[2]=='Z'||e[2]=='-'){res="HALT";break;}
   int ns=e[2]-'A';
   if(nl>M-4||nr>M-4){res="WIDE";break;}
   if(ns==st){long c;
     if(right){if(nr){c=R[nr-1].n;nr--;}else{res="AWAY";break;}push(L,&nl,w,c);}
     else{if(!nl&&v==0){res="AWAY";break;}pop1(R,&nr);c=1;if(nl&&L[nl-1].s==v){c+=L[nl-1].n;nl--;}push(R,&nr,w,c);int x=pop1(L,&nl);push(R,&nr,x,1);}
     steps+=c;
   }else{kept++;steps+=1;memmove(last[d],last[d]+1,(H-1)*sizeof(long));last[d][H-1]=kept;cnt[d]++;
     pop1(R,&nr);if(right)push(L,&nl,w,1);else{push(R,&nr,w,1);int x=pop1(L,&nl);push(R,&nr,x,1);}}
   st=ns;}
  // best digit: largest minimum of the last 6 gap ratios
  double best=0;int bd=-1;long bc=0;
  for(int d=0;d<14;d++){if(cnt[d]<H)continue;double mn=1e18;for(int i=H-7;i<H-2;i++){double g1=last[d][i+1]-last[d][i],g2=last[d][i+2]-last[d][i+1];double r=g2/g1;if(r<mn)mn=r;}
    if(mn>best){best=mn;bd=d;bc=cnt[d];}}
  long mx=0;for(int i=0;i<nl;i++)if(L[i].n>mx)mx=L[i].n;for(int i=0;i<nr;i++)if(R[i].n>mx)mx=R[i].n;
  printf("%s %s kept %ld log10steps %.1f runs %d maxblock %ld bestdigit %c count %ld minratio %.2f\n",t,res,kept,log10(steps+1),nl+nr,mx,bd<0?'-':"0123456789abcd"[bd],bc,best);}
}
