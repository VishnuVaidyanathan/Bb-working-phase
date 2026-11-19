/* story.c : from tape pictures to tables.
   A story is a list of pictures:   X 0111[0]11 -> Y 011[0]1111 300
   meaning: in state X with this tape (head on the bracketed cell), within 300 steps the machine
   must stand in state Y on that tape (same picture up to sliding along the tape).
   X, Y are names; the search decides which real state each is.  "-> HALT cap" asks for a halt.
   Usage: story NSTATES story.txt [maxsolutions]
   Prints every table (up to renaming of states) that plays all the pictures.  State 0 = the state of the first picture. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define W 160
#define MT 600
typedef struct{int sv,ev,halt,cap,head,lo,hi,nones,toff[W],tn,slack; char tape[W];}Test;
Test T[MT];int nt,N,used=1,var[26],maxsol=200000,nsol=0,haltset=0;long nodes=0;
int tr[8][2];/* -1 undefined, -2 halt, else w | m<<1 | ns<<2 */
typedef struct{char tape[W];int p,s,steps,ones;}Sim;
static void start(Sim*S,int t,int s){memcpy(S->tape,T[t].tape,W);S->p=T[t].head;S->s=s;S->steps=0;S->ones=T[t].nones;}
static int match(Sim*S,Test*t){if(S->ones!=t->tn)return 0;for(int i=0;i<t->tn;i++){int q=S->p+t->toff[i];if(q<0||q>=W||!S->tape[q])return 0;}return 1;}
static void out(void){char b[80];int k=0;for(int s=0;s<N;s++){for(int x=0;x<2;x++){int e=tr[s][x];if(e<0){b[k++]='-';b[k++]='-';b[k++]='-';}else{b[k++]='0'+(e&1);b[k++]=(e&2)?'R':'L';b[k++]='A'+(e>>2);}}if(s<N-1)b[k++]='_';}b[k]=0;
  for(int s=0;s<N;s++)for(int x=0;x<2;x++)if(tr[s][x]==-2){b[s*7+x*3]='1';b[s*7+x*3+1]='R';b[s*7+x*3+2]='Z';}
  printf("%s",b);for(int v=0;v<26;v++)if(var[v]>=0)printf(" %c=%c",'A'+v,'A'+var[v]);printf("\n");fflush(stdout);if(++nsol>=maxsol)exit(0);}
static void solve(int t,Sim S);
static void begin(int t){if(t==nt){out();return;}Sim S;int v=T[t].sv;
  if(var[v]>=0){start(&S,t,var[v]);solve(t,S);}
  else{int top=used<N?used:N-1;for(int s=0;s<=top;s++){int u=used;var[v]=s;if(s==used)used++;start(&S,t,s);solve(t,S);used=u;var[v]=-1;}}}
static void solve(int t,Sim S){Test*ts=&T[t];nodes++;
  for(;;){
    if(S.steps>0&&!ts->halt&&match(&S,ts)){int v=ts->ev;
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
    S.ones+=(e&1)-b;S.tape[S.p]=e&1;S.p+=(e&2)?1:-1;S.s=e>>2;S.steps++;
    if(S.p<ts->lo||S.p>ts->hi||(!ts->halt&&S.ones>ts->tn+ts->slack&&S.ones>ts->nones+ts->slack))return;
  }}
static int parse(const char*s,char*tape,int*head,int at){int n=0,h=-1;char c[W];for(;*s;s++){if(*s=='['){h=n;continue;}if(*s==']')continue;c[n++]=*s-'0';}
  memset(tape,0,W);for(int i=0;i<n;i++)tape[at-h+i]=c[i];*head=at;return n;}
int main(int ac,char**av){N=atoi(av[1]);FILE*f=fopen(av[2],"r");if(ac>3)maxsol=atoi(av[3]);char line[512];int slack=3,margin=3;
  for(int i=0;i<26;i++)var[i]=-1;for(int s=0;s<8;s++)tr[s][0]=tr[s][1]=-1;
  while(fgets(line,512,f)){char a[8],p1[200],arrow[8],b[8],p2[200];int cap;
    if(line[0]=='#'||line[0]=='\n')continue;
    if(sscanf(line,"slack %d",&slack)==1)continue; if(sscanf(line,"margin %d",&margin)==1)continue;
    Test*t=&T[nt];
    if(sscanf(line,"%s %s %s HALT %d",a,p1,arrow,&cap)==4&&strstr(line,"HALT")){t->halt=1;}
    else if(sscanf(line,"%s %s %s %s %s %d",a,p1,arrow,b,p2,&cap)==6){t->halt=0;t->ev=b[0]-'A';}
    else continue;
    t->sv=a[0]-'A';t->cap=cap;t->slack=slack;int n1=parse(p1,t->tape,&t->head,W/2);t->nones=0;for(int i=0;i<W;i++)t->nones+=t->tape[i];
    int n2=0;t->tn=0;
    if(!t->halt){char tt[W];int h;n2=parse(p2,tt,&h,W/2);for(int i=0;i<W;i++)if(tt[i])t->toff[t->tn++]=i-h;}
    int span=(n1>n2?n1:n2)+margin;t->lo=W/2-span;t->hi=W/2+span;if(t->lo<1)t->lo=1;if(t->hi>W-2)t->hi=W-2;nt++;}
  var[T[0].sv]=0;begin(0);fprintf(stderr,"solutions %d  nodes %ld\n",nsol,nodes);return 0;}
