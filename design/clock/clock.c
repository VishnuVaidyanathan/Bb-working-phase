// clock.c : the clock test, and the fill of the open wires of a hand-made skeleton.
//   clock TABLE            -> test one table
//   clock --fill SKELETON  -> SKELETON is a table with ??? for each open wire; every filling is tried (lazily: a wire is filled when first used)
// Clock test.  Run from a blank tape; find a visit "lead of k ones, 0, c words 10, short tail, head on the last 0 at the right end".
// Then thought experiments: build (k, c) with the same tail and state, run a short time:
//   H = halts;  g = comes back as (k', c');  R = no such visit again and the tape has grown (a row is being made; lead then = kr);  O = other.
// Follow: after R the next tick is (kr+1, 4).  Report the trace and the number of rows before a halt.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define NS 7
#define TS 65536
typedef struct{signed char w,m,n;}Wire;            // n: -1 halt, -2 open
static Wire T[NS][2];
static unsigned char tp[TS];
static void show(char*o){for(int q=0;q<NS;q++){for(int b=0;b<2;b++){Wire x=T[q][b];if(x.n==-1){*o++='-';*o++='-';*o++='-';}else if(x.n==-2){*o++='?';*o++='?';*o++='?';}else{*o++='0'+x.w;*o++=x.m>0?'R':'L';*o++='A'+x.n;}}if(q<NS-1)*o++='_';}*o=0;}
static void parse(const char*s){for(int q=0;q<NS;q++)for(int b=0;b<2;b++){const char*e=s+q*7+b*3;if(e[2]=='-'||e[2]=='Z')T[q][b].n=-1;else if(e[2]=='?')T[q][b].n=-2;else{T[q][b].w=e[0]-'0';T[q][b].m=e[1]=='R'?1:-1;T[q][b].n=e[2]-'A';}}}
// lone form on tape cells [a..p]: 1^k 0 (10)^c tail ; returns 1 and fills k,c,tail
static int lone(int a,int p,int*k,int*c,unsigned char*tail,int*tl){
  int i=a;while(i<=p&&!tp[i])i++; int s=i;while(i<=p&&tp[i])i++; *k=i-s; if(*k<1||i>p)return 0; i++;      // the single 0
  int n=0;while(i+1<=p&&tp[i]==1&&tp[i+1]==0&&i+2<=p&&!(tp[i+2]==0)){n++;i+=2;}                           // words 10 followed by a 1
  // the last word 10 before the tail: accept it too if the tail then starts with 1
  *c=n; int L=p-i+1; if(n<2||L<1||L>12)return 0; memcpy(tail,tp+i,L);*tl=L; return 1;}
static int s0,tl0;static unsigned char tail0[16];
// one thought experiment
static char tick(int k,int c,int*k2,int*c2,long B){
  if(k>300||c>300||k<1)return 'O';
  memset(tp,0,TS);int a=TS/2,i=a;for(int j=0;j<k;j++)tp[i++]=1;i++;for(int j=0;j<c;j++){tp[i]=1;i+=2;}memcpy(tp+i,tail0,tl0);i+=tl0;
  int pos=i-1,st=s0,lo=a,hi=pos,len0=hi-lo;
  for(long t=0;t<B;t++){int b=tp[pos];
    if(t>0&&st==s0&&b==0&&pos==hi){int kk,cc,tl;unsigned char tt[16];if(lone(lo,pos,&kk,&cc,tt,&tl)&&tl==tl0&&!memcmp(tt,tail0,tl)){*k2=kk;*c2=cc;return 'g';}}
    Wire x=T[st][b];if(x.n<0)return 'H';tp[pos]=x.w;pos+=x.m;st=x.n;if(pos<lo)lo=pos;if(pos>hi)hi=pos;if(pos<4||pos>TS-4)break;}
  if(hi-lo>len0+30){int j=lo;while(j<=hi&&!tp[j])j++;int s=j;while(j<=hi&&tp[j])j++;*k2=j-s;return 'R';}
  return 'O';}
static long nfull=0,nlone=0,n1=0,n2=0;
static void full(int verbose){
  nfull++;memset(tp,0,TS);int pos=TS/2,st=0,lo=pos,hi=pos;int k0=0,c0=0,found=0;
  for(long t=0;t<300000;t++){int b=tp[pos];
    if(b==0&&pos==hi&&hi-lo<=120&&hi-lo>=8){int tl;if(lone(lo,pos,&k0,&c0,tail0,&tl)){tl0=tl;s0=st;found=1;break;}}
    Wire x=T[st][b];if(x.n<0)return;tp[pos]=x.w;pos+=x.m;st=x.n;if(pos<lo)lo=pos;if(pos>hi)hi=pos;if(pos<4||pos>TS-4)return;}
  if(!found){if(verbose)printf("no lone-counter visit found\n");return;}
  nlone++;char tr[64];int n=0,rows=0,k=k0,c=c0;char end='?';
  for(int it=0;it<12;it++){int k2=0,c2=0;char o=tick(k,c,&k2,&c2,60000);
    if(o=='H'){tr[n++]='H';end='H';break;}
    if(o=='g'){tr[n++]='g';if(c2>60||(k2==k&&c2==c)){end='o';break;}k=k2;c=c2;continue;}
    if(o=='R'){tr[n++]='R';rows++;k=k2+1;c=4;continue;}
    tr[n++]='O';end='O';break;}
  tr[n]=0;
  if(end=='H'&&rows==1)n1++;
  if(end=='H'&&rows>=2)n2++;
  if(verbose||(end=='H'&&rows>=1)){char s[64];show(s);printf("%s | rows %d | %s | boot lead %d counter %d state %c\n",s,rows,tr,k0,c0,'A'+s0);fflush(stdout);}}
// lazy fill
typedef struct{int pos,st,lo,hi;long t;}Cfg;
static long nodes=0,rej_unused=0,rej_halt=0;
static void dfs(unsigned char*tape,Cfg c){
  nodes++;
  for(;c.t<5000;c.t++){int b=tape[c.pos];Wire x=T[c.st][b];
    if(x.n==-1){rej_halt++;return;}
    if(x.n==-2){unsigned char*cp=malloc(4096);
      for(int w=0;w<2;w++)for(int m=-1;m<=1;m+=2)for(int n=0;n<NS;n++){T[c.st][b].w=w;T[c.st][b].m=m;T[c.st][b].n=n;memcpy(cp,tape,4096);dfs(cp,c);}
      T[c.st][b].n=-2;free(cp);return;}
    tape[c.pos]=x.w;c.pos+=x.m;c.st=x.n;if(c.pos<c.lo)c.lo=c.pos;if(c.pos>c.hi)c.hi=c.pos;if(c.pos<4||c.pos>4092)break;}
  for(int q=0;q<NS;q++)for(int b=0;b<2;b++)if(T[q][b].n==-2){rej_unused++;return;}
  if(c.hi-c.lo<12)return;
  full(0);}
int main(int ac,char**av){
  if(ac==3&&!strcmp(av[1],"--fill")){parse(av[2]);unsigned char*tape=calloc(4096,1);Cfg c={2048,0,2048,2048,0};dfs(tape,c);
    fprintf(stderr,"nodes %ld  halted early %ld  a wire unused %ld  full tests %ld  with a lone-counter visit %ld  one row then halt %ld  two+ rows then halt %ld\n",nodes,rej_halt,rej_unused,nfull,nlone,n1,n2);return 0;}
  parse(av[1]);full(1);return 0;}
