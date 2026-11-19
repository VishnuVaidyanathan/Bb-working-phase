/* free.c : from loose tape pictures to tables.
   A picture gives only the tape before and after, drawn in the same place (same length, pad with 0),
   the most head turns allowed, and the most steps.  The search invents the passes.
       S 0[0]0011000  S 0[0]1111110  1 30        state S on tape 1  ->  state S on tape 2, at most 1 turn, 30 steps
       S 00[0]1100    HALT           2 40        must halt within 2 turns and 40 steps
   Usage: free NSTATES file [maxsolutions [STARTTABLE]]   (STARTTABLE: keep these entries, invent the rest)     State names are only names; the search decides the real states. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define W 128
#define MT 400
typedef struct{int sv,ev,halt,cap,K,head,thead,n;char tape[W],tgt[W];}Test;
Test T[MT];int nt,N,used=1,var[26],maxsol=100000,nsol=0,haltset=0;long nodes=0;int tr[8][2];
typedef struct{char tape[W];int p,s,steps,dir,turns;}Sim;
static void out(void){char b[80];int k=0;for(int s=0;s<N;s++){for(int x=0;x<2;x++){int e=tr[s][x];if(e==-2){b[k++]='1';b[k++]='R';b[k++]='Z';}else if(e<0){b[k++]='-';b[k++]='-';b[k++]='-';}else{b[k++]='0'+(e&1);b[k++]=(e&2)?'R':'L';b[k++]='A'+(e>>2);}}if(s<N-1)b[k++]='_';}b[k]=0;
  printf("%s",b);for(int v=0;v<26;v++)if(var[v]>=0)printf(" %c=%c",'A'+v,'A'+var[v]);printf("\n");fflush(stdout);if(++nsol>=maxsol)exit(0);}
static void solve(int t,Sim S);
static void begin(int t){if(t==nt){out();return;}Sim S;int v=T[t].sv;memcpy(S.tape,T[t].tape,W);S.p=T[t].head;S.steps=0;S.dir=0;S.turns=0;
  if(var[v]>=0){S.s=var[v];solve(t,S);}
  else{int top=used<N?used:N-1;for(int s=0;s<=top;s++){int u=used;var[v]=s;if(s==used)used++;S.s=s;solve(t,S);used=u;var[v]=-1;}}}
static int farside_ok(Sim*S,Test*ts,int d){ /* cells the head can never reach again must already be right */
  if(d<0){for(int i=S->p+1;i<ts->n;i++)if(S->tape[i]!=ts->tgt[i])return 0;return ts->thead<=S->p;}
  for(int i=0;i<S->p;i++)if(S->tape[i]!=ts->tgt[i])return 0;return ts->thead>=S->p;}
static void solve(int t,Sim S){Test*ts=&T[t];nodes++;
  for(;;){
    if(S.steps>0&&!ts->halt&&S.p==ts->thead&&!memcmp(S.tape,ts->tgt,ts->n)){int v=ts->ev;
      if(var[v]==S.s){begin(t+1);return;}
      if(var[v]<0){var[v]=S.s;begin(t+1);var[v]=-1;}}
    if(S.steps>=ts->cap)return;
    int b=S.tape[S.p],e=tr[S.s][b];
    if(e==-2){if(ts->halt)begin(t+1);return;}
    if(e==-1){
      if(ts->halt&&!haltset){tr[S.s][b]=-2;haltset=1;begin(t+1);haltset=0;tr[S.s][b]=-1;}
      int top=used<N?used:N-1;
      for(int ns=0;ns<=top;ns++)for(int w=0;w<2;w++)for(int m=0;m<2;m++){int u=used;if(ns==used)used++;tr[S.s][b]=w|(m<<1)|(ns<<2);solve(t,S);tr[S.s][b]=-1;used=u;}
      return;}
    int d=(e&2)?1:-1;
    if(S.dir&&d!=S.dir){if(++S.turns>ts->K)return;}
    S.tape[S.p]=e&1;
    if(!ts->halt&&S.turns==ts->K){if(S.dir!=d||S.steps==0){S.dir=d;if(!farside_ok(&S,ts,d))return;}
      if(S.tape[S.p]!=ts->tgt[S.p])return;}
    S.dir=d;S.p+=d;S.s=e>>2;S.steps++;
    if(S.p<0||S.p>=ts->n)return;
  }}
static int parse(const char*s,char*tape,int*head){int n=0;for(;*s;s++){if(*s=='['){*head=n;continue;}if(*s==']')continue;tape[n++]=*s-'0';}return n;}
int main(int ac,char**av){N=atoi(av[1]);FILE*f=fopen(av[2],"r");if(ac>3)maxsol=atoi(av[3]);char line[600];
  for(int i=0;i<26;i++)var[i]=-1;for(int s=0;s<8;s++)tr[s][0]=tr[s][1]=-1;
  while(fgets(line,600,f)){char a[8],p1[200],b[8],p2[200];int K,cap;if(line[0]=='#'||line[0]=='\n')continue;Test*t=&T[nt];
    if(sscanf(line,"%s %s HALT %d %d",a,p1,&K,&cap)==4){t->halt=1;t->n=parse(p1,t->tape,&t->head);}
    else if(sscanf(line,"%s %s %s %s %d %d",a,p1,b,p2,&K,&cap)==6){t->halt=0;t->ev=b[0]-'A';t->n=parse(p1,t->tape,&t->head);int n2=parse(p2,t->tgt,&t->thead);if(n2!=t->n){fprintf(stderr,"picture %d: the two tapes must have the same length\n",nt+1);return 1;}}
    else continue;
    t->sv=a[0]-'A';t->K=K;t->cap=cap;nt++;}
  if(ac>4){char*t=av[4];int n=(strlen(t)+1)/7;used=n;for(int q=0;q<n;q++)for(int x=0;x<2;x++){char*e=t+q*7+x*3;if(e[2]=='-')tr[q][x]=-1;else if(e[2]=='Z'){tr[q][x]=-2;haltset=1;}else tr[q][x]=(e[0]-'0')|((e[1]=='R')<<1)|((e[2]-'A')<<2);}}
  var[T[0].sv]=0;begin(0);fprintf(stderr,"solutions %d  nodes %ld\n",nsol,nodes);return 0;}
