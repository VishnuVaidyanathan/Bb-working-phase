// Cousins from roles, any number of states (used for BB(7)).
// usage: roles7 NS SKELETON MINSTEPS [CAP]
//   SKELETON: 2*NS letters, the next state of each wire in order A0 A1 B0 B1 ..., or '?' = free.
//   e.g. champion skeleton for BB(7):  BGCBD?EDFEAFCB   (C1 is the halt in the champion: left free)
// Everything else is free: what each wire writes, which way it moves.  A wire is filled in only when the run
// from a blank tape reaches it; reaching an empty wire is the halt.  One wire always stays empty.
// Prints "H steps ones table" for halts after >= MINSTEPS steps, and "R width table" for tables that are still
// running at CAP steps and are not a regular bouncer.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <signal.h>
#include <unistd.h>
#define TS (1<<18)
static unsigned char t[TS];
int NS; long CAP=20000000L, MINS=1000;
int W[8][2],D[8][2],X[8][2],def[8][2],fix[8][2]; long nodes=0,surv=0,bkill=0,nh=0,nr=0;
void name(char*buf){int k=0; for(int s=0;s<NS;s++){ for(int b=0;b<2;b++){ if(def[s][b]){buf[k++]='0'+W[s][b];buf[k++]=D[s][b]>0?'R':'L';buf[k++]='A'+X[s][b];} else {buf[k++]='-';buf[k++]='-';buf[k++]='-';} } buf[k++]='_';} buf[k-1]=0;}
void rep(int x){ char b[64]; name(b); fprintf(stderr,"nodes %ld to2M %ld regular %ld halts %ld running %ld at %s\n",nodes,surv,bkill,nh,nr,b); alarm(60);}
#define NE 4000
static long ev[2][NE]; static int ne[2];
int regular(long*e,int n){ if(n<24) return 1; static long d[NE]; int m=0; for(int i=1;i<n;i++) d[m++]=e[i]-e[i-1];
  for(int p=1;p<=64&&3*p<m;p++){ int ok=1; for(int i=2*p;i<m;i++) if(d[i]-d[i-p]!=d[i-p]-d[i-2*p]){ok=0;break;} if(ok) return 1; } return 0; }
int pre[16],npre=0;
void dfs(int nund){
  nodes++;
  int pos=TS/2,st=0,lo=pos,hi=pos; long s; int us=-1,ub=-1; int dead=0; ne[0]=ne[1]=0;
  for(s=0;s<CAP;s++){ int b=t[pos]; if(!def[st][b]){us=st;ub=b;break;}
    t[pos]=W[st][b]; pos+=D[st][b]; st=X[st][b];
    if(pos<lo){lo=pos; if(s>=200000&&s<2000000&&ne[0]<NE) ev[0][ne[0]++]=s; if(pos<4){dead=1;break;}}
    else if(pos>hi){hi=pos; if(s>=200000&&s<2000000&&ne[1]<NE) ev[1][ne[1]++]=s; if(pos>TS-4){dead=1;break;}}
    if(s==300){ if(hi-lo<8){dead=1;break;} }
    else if(s==3000){ int w=hi-lo; if(w<20||w>1000){dead=1;break;} }
    else if(s==20000){ int w=hi-lo; if(w<40||w>3000){dead=1;break;} }
    else if(s==200000){ int w=hi-lo; if(w<80||w>8000){dead=1;break;} }
    else if(s==2000000){ surv++; if(regular(ev[0],ne[0])&&regular(ev[1],ne[1])){bkill++;dead=1;break;} } }
  long ones=0; for(int i=lo;i<=hi;i++)ones+=t[i];
  memset(t+lo-1,0,hi-lo+3);
  if(dead) return;
  char buf[64];
  if(us<0){ name(buf); nr++; printf("R %d %s\n",hi-lo,buf); fflush(stdout); return; }
  if(s>=MINS){ name(buf); nh++; printf("H %ld %ld %s\n",s+1,ones,buf); fflush(stdout); }
  if(nund<=1) return;
  def[us][ub]=1;
  for(int w=0;w<2;w++) for(int d=-1;d<=1;d+=2){
    if(nund==2*NS && d!=1) continue;
    { int dep=2*NS-nund; if(dep<npre && pre[dep]!=w*2+(d>0)) continue; }
    W[us][ub]=w; D[us][ub]=d;
    if(fix[us][ub]>=0){ X[us][ub]=fix[us][ub]; dfs(nund-1); }
    else for(int n=0;n<NS;n++){ X[us][ub]=n; dfs(nund-1); } }
  def[us][ub]=0;
}
int main(int argc,char**argv){ NS=atoi(argv[1]); char*sk=argv[2]; MINS=atol(argv[3]); if(argc>4) CAP=atol(argv[4]);
  for(int i=0;i<2*NS;i++) fix[i/2][i%2]= sk[i]=='?'?-1:sk[i]-'A';
  { char*p=getenv("PRE"); if(p) for(;*p;p++) pre[npre++]=*p-'0'; }
  signal(SIGALRM,rep); alarm(60); dfs(2*NS);
  printf("DONE tables tried: %ld  reached 2M steps: %ld  regular: %ld  halts>=%ld: %ld  still running at %ld: %ld\n",nodes,surv,bkill,MINS,nh,CAP,nr); }
