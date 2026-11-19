/* ext.c M BUDGET : BB(5)'s engine with its halt road left open and two new states (5 free wires).
   Start: a BB(5) layer with M short pieces, run by BB(5)'s table until the halt road (state E reads 0).
   From there every way of filling the free wires is tried, as far as the run needs them.
   An unfilled wire that is reached counts as the halt.  Prints one line per outcome. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define W 400000
#define NS 7
int tr[NS][2];long BUD;static char T0[W];int P0,S0;long LO0,HI0;
typedef struct{char*t;long p,lo,hi,steps,walls,ones;int s,prev;}Sim;
static void name(char*b){int k=0;for(int s=0;s<NS;s++){for(int x=0;x<2;x++){int e=tr[s][x];if(e<0){b[k++]='-';b[k++]='-';b[k++]='-';}else{b[k++]='0'+(e&1);b[k++]=(e&2)?'R':'L';b[k++]='A'+(e>>2);}}if(s<NS-1)b[k++]='_';}b[k]=0;}
static void rec(Sim S,int used){
  char*t=S.t;long winlo=S.p,winhi=S.p,wins=S.steps;
  for(;;){
    int b=t[S.p],e=tr[S.s][b];
    if(e<0){char nm[80];
      /* this wire as the halt */
      name(nm);printf("HALT %s steps %ld walls %ld ones %ld\n",nm,S.steps,S.walls,S.ones);
      int top=used<NS?used:NS-1;
      for(int ns=0;ns<=top;ns++)for(int w=0;w<2;w++)for(int m=0;m<2;m++){
        tr[S.s][b]=w|(m<<1)|(ns<<2);Sim C=S;C.t=malloc(W);memcpy(C.t,t,W);rec(C,ns==used?used+1:used);free(C.t);tr[S.s][b]=-1;}
      return;}
    int d=2*S.s+b; if(S.prev==4&&d==6)S.walls++; S.prev=d;
    S.ones+=(e&1)-b;t[S.p]=e&1;S.p+=(e&2)?1:-1;S.s=e>>2;S.steps++;
    if(S.p<S.lo)S.lo=S.p; if(S.p>S.hi)S.hi=S.p;
    if(S.p<winlo)winlo=S.p; if(S.p>winhi)winhi=S.p;
    if(S.steps-wins>=4000){ if(winhi-winlo<12){return;} winlo=winhi=S.p;wins=S.steps;}     /* stuck in a small place: dead */
    if(S.p<50||S.p>W-50)return;                                                          /* off the tape: runaway */
    if(S.steps>=BUD){char nm[80];name(nm);printf("ALIVE %s steps %ld walls %ld ones %ld span %ld\n",nm,S.steps,S.walls,S.ones,S.hi-S.lo);return;}
  }}
int main(int ac,char**av){int M=atoi(av[1]);BUD=atol(av[2]);
  const char*bb="1RB1LC_1RC1RB_1RD0LE_1LA1LD_---0LA";for(int s=0;s<NS;s++)tr[s][0]=tr[s][1]=-1;
  for(int s=0;s<5;s++)for(int x=0;x<2;x++){const char*e=bb+s*7+x*3;tr[s][x]=e[2]=='-'?-1:(e[0]-'0')|((e[1]=='R')<<1)|((e[2]-'A')<<2);}
  Sim S;S.t=calloc(W,1);long p=W/2;S.p=p;long q=p+1;for(int i=0;i<M;i++){q+=2;S.t[q++]=1;}S.t[q]=1; /* [0] (001)^M 1 */
  S.s=0;S.steps=0;S.walls=0;S.prev=-1;S.lo=S.hi=p;S.ones=M+1;
  /* run plain BB5 to its halt road */
  for(;;){int b=S.t[S.p],e=tr[S.s][b];if(e<0)break;S.ones+=(e&1)-b;S.t[S.p]=e&1;S.p+=(e&2)?1:-1;S.s=e>>2;S.steps++;if(S.steps>2000000000L){fprintf(stderr,"no halt road\n");return 1;}}
  fprintf(stderr,"halt road reached after %ld steps, ones %ld, state %c\n",S.steps,S.ones,'A'+S.s);
  S.steps=0;rec(S,5);return 0;}
