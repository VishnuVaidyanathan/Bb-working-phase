// fillgate.c SKELETON : fill the open wires (???) of a hand-made skeleton, lazily, and keep the tables that
//   (1) use every wire and do not halt in the first 5,000 steps, (2) do not halt within 1,000,000 steps from a blank tape,
//   (3) HALT on some small tapes of their own form (their own right-end visits with the repeat counts shrunk): a gate that can fire.
// Output: table | small tapes that halt / tried | cells used after 1,000,000 steps.     fillgate --one TABLE tests one table.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define NS 7
#define TS 65536
typedef struct{signed char w,m,n;}Wire;
static Wire T[NS][2];
static unsigned char tp[TS],t2[TS];
static unsigned rs=12345;static unsigned rnd(){rs=rs*1103515245u+12345u;return (rs>>16)&0x7fff;}
static void show(char*o){for(int q=0;q<NS;q++){for(int b=0;b<2;b++){Wire x=T[q][b];if(x.n==-1){*o++='-';*o++='-';*o++='-';}else if(x.n==-2){*o++='?';*o++='?';*o++='?';}else{*o++='0'+x.w;*o++=x.m>0?'R':'L';*o++='A'+x.n;}}if(q<NS-1)*o++='_';}*o=0;}
static void parse(const char*s){for(int q=0;q<NS;q++)for(int b=0;b<2;b++){const char*e=s+q*7+b*3;if(e[2]=='-'||e[2]=='Z')T[q][b].n=-1;else if(e[2]=='?')T[q][b].n=-2;else{T[q][b].w=e[0]-'0';T[q][b].m=e[1]=='R'?1:-1;T[q][b].n=e[2]-'A';}}}
#define MW 3000
static int wa[MW],wb[MW],wk[MW];
static int trial(int lo,int hi,int st){            // perturb tp[lo..hi] (head at hi, reading 0) into t2 and run
  int n=0,i=lo;while(i<=hi&&!tp[i])i++;
  while(i<=hi){int a=0,b=0;while(i<=hi&&tp[i]){a++;i++;}while(i<=hi&&!tp[i]){b++;i++;}
    if(n&&wa[n-1]==a&&wb[n-1]==b)wk[n-1]++;else{if(n>=MW)return 0;wa[n]=a;wb[n]=b;wk[n]=1;n++;}}
  if(!n)return 0;
  memset(t2,0,TS);int p=TS/2;
  for(int j=0;j<n;j++){int a=wa[j]<=8?wa[j]:1+rnd()%8;int k=wk[j]==1?1:1+rnd()%(wk[j]<7?wk[j]:7);
    for(int r=0;r<k;r++){for(int c=0;c<a;c++)t2[p++]=1;p+=wb[j];if(p>TS-100)return 0;}}
  int pos=p-1;if(t2[pos])pos++;
  for(int t=0;t<20000;t++){int b=t2[pos];Wire x=T[st][b];if(x.n<0)return 1;t2[pos]=x.w;pos+=x.m;st=x.n;if(pos<4||pos>TS-4)return 0;}
  return 0;}
static long nleaf=0,nrun=0,nselfhalt=0,ngate=0;
static void leaf(int verbose){
  nleaf++;memset(tp,0,TS);int pos=TS/2,st=0,lo=pos,hi=pos;long next=2000;int halts=0,tried=0;
  for(long t=0;t<1000000;t++){int b=tp[pos];
    if(b==0&&pos==hi&&t>=next&&hi-lo<20000){next*=2;for(int r=0;r<20;r++){tried++;halts+=trial(lo,hi,st);}}
    Wire x=T[st][b];if(x.n<0){nselfhalt++;if(verbose||t>100000){char s[64];show(s);printf("%s | HALTS by itself at step %ld\n",s,t+1);}return;}
    tp[pos]=x.w;pos+=x.m;st=x.n;if(pos<lo)lo=pos;if(pos>hi)hi=pos;if(pos<4||pos>TS-4)break;}
  nrun++;
  if(halts>0||verbose){ngate+=halts>0;char s[64];show(s);printf("%s | %d/%d | %d\n",s,halts,tried,hi-lo);fflush(stdout);}}
typedef struct{int pos,st,lo,hi;long t;}Cfg;
static long nodes=0;
static void dfs(unsigned char*tape,Cfg c){
  nodes++;
  for(;c.t<5000;c.t++){int b=tape[c.pos];Wire x=T[c.st][b];
    if(x.n==-1)return;
    if(x.n==-2){unsigned char*cp=malloc(4096);
      for(int w=0;w<2;w++)for(int m=-1;m<=1;m+=2)for(int n=0;n<NS;n++){T[c.st][b].w=w;T[c.st][b].m=m;T[c.st][b].n=n;memcpy(cp,tape,4096);dfs(cp,c);}
      T[c.st][b].n=-2;free(cp);return;}
    tape[c.pos]=x.w;c.pos+=x.m;c.st=x.n;if(c.pos<c.lo)c.lo=c.pos;if(c.pos>c.hi)c.hi=c.pos;if(c.pos<4||c.pos>4092)break;}
  for(int q=0;q<NS;q++)for(int b=0;b<2;b++)if(T[q][b].n==-2)return;
  if(c.hi-c.lo<12)return;
  leaf(0);}
int main(int ac,char**av){
  if(ac==3&&!strcmp(av[1],"--one")){parse(av[2]);leaf(1);return 0;}
  parse(av[1]);unsigned char*tape=calloc(4096,1);Cfg c={2048,0,2048,2048,0};dfs(tape,c);
  fprintf(stderr,"branches %ld  tables tested %ld  halt by themselves %ld  run on %ld  with a gate that fires %ld\n",nodes,nleaf,nselfhalt,nrun,ngate);return 0;}
