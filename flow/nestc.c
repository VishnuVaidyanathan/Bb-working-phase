/* nestc.c STEPS [MINDEPTH [MINSPAN]] : reads tables (first word of each line) and keeps those that pass the nest test.
   Runs each from a blank tape, finds the most used loop (a digit that repeats, or two that alternate), lists the length
   of each of its runs, and counts how many times "climb, fall back, look at the tops" can be repeated (see nest.py).
   Keeps a table if that nest depth is at least MINDEPTH (3) and the tape has grown to at least MINSPAN cells (100).
   Prints: table, nest depth, tape span, the loop, number of runs. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define W 400000
static char tape[W];static unsigned char *tr_;static int R[4000000];
static int tops(int*s,int n,int*o){int k=0,rising=1,have=0,m=0,lo=0;for(int i=0;i<n;i++){int x=s[i];
    if(rising){if(!have||x>m){m=x;have=1;}else if(10*x<=7*m){o[k++]=m;rising=0;lo=x;}}
    else{if(x<lo)lo=x;else if(7*x>=10*lo){rising=1;m=x;}}}return k;}
int main(int ac,char**av){long NS=atol(av[1]);int MD=ac>2?atoi(av[2]):3,MS=ac>3?atoi(av[3]):100;char line[4096];
  tr_=malloc(NS+1);
  while(fgets(line,4096,stdin)){char t[64];if(sscanf(line,"%60s",t)!=1||strlen(t)<48)continue;int tr[7][2];
    for(int s=0;s<7;s++)for(int b=0;b<2;b++){char*e=t+s*7+b*3;tr[s][b]=(e[2]=='-'||e[2]=='Z')?-1:(e[0]-'0')|((e[1]=='R')<<1)|((e[2]-'A')<<2);}
    memset(tape,0,W);long p=W/2,lo=p,hi=p,n=0;int s=0;static long pc[14][14];memset(pc,0,sizeof(pc));int prev=-1;
    for(;n<NS;n++){int b=tape[p],d=2*s+b;tr_[n]=d;if(prev>=0)pc[prev][d]++;prev=d;int e=tr[s][b];if(e<0){n++;break;}
      tape[p]=e&1;p+=(e&2)?1:-1;s=e>>2;if(p<lo)lo=p;if(p>hi)hi=p;if(p<5||p>W-5)break;}
    /* the most used loop */
    long best=0;int la=-1,lb=-1;
    for(int a=0;a<14;a++){if(pc[a][a]>best){best=pc[a][a];la=lb=a;}
      for(int b=0;b<14;b++)if(a!=b&&pc[a][b]>0&&pc[b][a]*10>pc[a][b]*8&&pc[a][b]+pc[b][a]>best){best=pc[a][b]+pc[b][a];la=a;lb=b;}}
    if(la<0)continue;
    int nr=0;
    if(la==lb){long i=0;while(i<n){if(tr_[i]==la){long j=i;while(j<n&&tr_[j]==la)j++;if(j-i>=2&&nr<4000000)R[nr++]=j-i;i=j;}else i++;}}
    else{long i=0;while(i+1<n){if(tr_[i]==la&&tr_[i+1]==lb){long j=i;int c=0;while(j+1<n&&tr_[j]==la&&tr_[j+1]==lb){c++;j+=2;}if(c>=2&&nr<4000000)R[nr++]=c;i=j;}else i++;}}
    int depth=1,len=nr;static int A[4000000];int*cur=R;
    while(1){int k=tops(cur,len,A);if(k<2)break;depth++;memcpy(R,A,k*sizeof(int));cur=R;len=k;if(depth>20)break;}
    if(depth>=MD&&hi-lo>=MS){const char*H="0123456789abcd";if(la==lb)printf("%s %d %ld %c %d\n",t,depth,hi-lo,H[la],nr);else printf("%s %d %ld %c%c %d\n",t,depth,hi-lo,H[la],H[lb],nr);fflush(stdout);}
  }return 0;}
