// Cousins from roles, BB(5), with cheap early filters.
// usage: roles2 F1 F2 O1 O2 O3 [A0write A0next]   (optional split of the search on the first wire)
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <signal.h>
#include <unistd.h>
long nodes=0,surv=0,bkill=0,nh=0;
#define TS (1<<17)
#define LMAX 60000000L
static unsigned char t[TS];
int W[5][2],D[5][2],X[5][2],def[5][2]; int one_next[5];  int fw=-1,fn=-1;
void rep(int x);
void name(char*buf){int k=0; for(int s=0;s<5;s++){ for(int b=0;b<2;b++){ if(def[s][b]){buf[k++]='0'+W[s][b];buf[k++]=D[s][b]>0?'R':'L';buf[k++]='A'+X[s][b];} else {buf[k++]='-';buf[k++]='-';buf[k++]='-';} } buf[k++]='_';} buf[k-1]=0;}
#define NE 4000
static long ev[2][NE]; static int ne[2];
// a side is "regular" if the second differences of its record times repeat with a short period
int regular(long*e,int n){ if(n<24) return 1; static long d[NE]; int m=0; for(int i=1;i<n;i++) d[m++]=e[i]-e[i-1];
  for(int p=1;p<=64&&3*p<m;p++){ int ok=1; for(int i=2*p;i<m;i++) if(d[i]-d[i-p]!=d[i-p]-d[i-2*p]){ok=0;break;} if(ok) return 1; } return 0; }
void dfs(int nund){
  nodes++;
  int pos=TS/2,st=0,lo=pos,hi=pos; long s; int us=-1,ub=-1; int dead=0; ne[0]=ne[1]=0;
  for(s=0;s<LMAX;s++){ int b=t[pos]; if(!def[st][b]){us=st;ub=b;break;}
    t[pos]=W[st][b]; pos+=D[st][b]; st=X[st][b];
    if(pos<lo){lo=pos; if(s>=200000&&s<2000000&&ne[0]<NE) ev[0][ne[0]++]=s; if(pos<4){dead=1;break;}}
    else if(pos>hi){hi=pos; if(s>=200000&&s<2000000&&ne[1]<NE) ev[1][ne[1]++]=s; if(pos>TS-4){dead=1;break;}}
    if(s==300){ if(hi-lo<8){dead=1;break;} }
    else if(s==3000){ int w=hi-lo; if(w<30||w>1000){dead=1;break;} }
    else if(s==20000){ int w=hi-lo; if(w<80||w>3000){dead=1;break;} }
    else if(s==200000){ int w=hi-lo; if(w<250||w>8000){dead=1;break;} }
    else if(s==2000000){ surv++; if( (regular(ev[0],ne[0])&&regular(ev[1],ne[1]))){bkill++;dead=1;break;} } }
  long ones=0; if(us>=0) for(int i=lo;i<=hi;i++)ones+=t[i];
  memset(t+lo-1,0,hi-lo+3);
  if(us<0||dead) return;
  if(s>=100000){ char buf[40]; name(buf); nh++; printf("%ld %ld %s\n",s+1,ones,buf); fflush(stdout); }
  if(nund<=1) return;
  def[us][ub]=1;
  for(int w=0;w<2;w++) for(int d=-1;d<=1;d+=2){
    if(nund==10 && d!=1) continue;
    W[us][ub]=w; D[us][ub]=d;
    if(ub==1){ X[us][ub]=one_next[us]; dfs(nund-1); }
    else for(int n=0;n<5;n++){ if(nund==10&&fw>=0&&(w!=fw||n!=fn)) continue; X[us][ub]=n; dfs(nund-1); } }
  def[us][ub]=0;
}
void rep(int x){ char b[40]; name(b); fprintf(stderr,"nodes %ld surv %ld bkill %ld nh %ld at %s\n",nodes,surv,bkill,nh,b); alarm(20);} 
int main(int argc,char**argv){ int f1=argv[1][0]-'A',f2=argv[2][0]-'A',o1=argv[3][0]-'A',o2=argv[4][0]-'A',o3=argv[5][0]-'A';
  if(argc>7){fw=atoi(argv[6]);fn=argv[7][0]-'A';}
  one_next[f1]=f1; one_next[f2]=f2; one_next[o1]=o2; one_next[o2]=o3; one_next[o3]=o1;
  signal(SIGALRM,rep); alarm(20); dfs(10); fprintf(stderr,"tables tried: %ld  reached 2M steps: %ld  thrown out as regular: %ld  halting after 100,000 steps: %ld\n",nodes,surv,bkill,nh); }
