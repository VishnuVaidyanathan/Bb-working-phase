/* zonec.c STEPS : the zones of a machine, in roads (a road = one digit followed by another).
   Reads tables (first word of each line), runs each from a blank tape and prints
     table  small  river  next  fillers  rivercount  growth
   river   = the biggest group of roads used about equally often (neighbours within 8 percent), loops left out
   small   = roads used less often than the river        next = roads used more often than the river, not loops
   fillers = loops (a digit repeating, or two digits alternating) used at least 20 times as often as the river
   growth  = (filler per river round at the end) / (the same at a quarter of the run); 2 is a plain back-and-forth */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define W 400000
static char tape[W];typedef struct{long n;int a,b;}Rd;
static int cmp(const void*x,const void*y){long a=((Rd*)x)->n,b=((Rd*)y)->n;return a<b?-1:a>b;}
int main(int ac,char**av){long NS=atol(av[1]);char line[4096];
  while(fgets(line,4096,stdin)){char t[64];if(sscanf(line,"%60s",t)!=1||strlen(t)<48)continue;int tr[7][2];
    for(int s=0;s<7;s++)for(int b=0;b<2;b++){char*e=t+s*7+b*3;tr[s][b]=(e[2]=='-'||e[2]=='Z')?-1:(e[0]-'0')|((e[1]=='R')<<1)|((e[2]-'A')<<2);}
    memset(tape,0,W);long p=W/2;int s=0,prev=-1;static long pc[14][14],q[14][14];memset(pc,0,sizeof(pc));memset(q,0,sizeof(q));
    for(long n=0;n<NS;n++){int b=tape[p],d=2*s+b;if(prev>=0)pc[prev][d]++;prev=d;int e=tr[s][b];if(e<0)break;tape[p]=e&1;p+=(e&2)?1:-1;s=e>>2;if(p<5||p>W-5)break;if(n==NS/4)memcpy(q,pc,sizeof(pc));}
    Rd v[200];int n=0;long fill[20],qfill[20];int nf=0;
    for(int a=0;a<14;a++)for(int b=0;b<14;b++){long c=pc[a][b];if(!c)continue;
      int loop=(a==b)||(pc[b][a]*10>c*8&&c*10>pc[b][a]*8);
      if(loop){if(a<=b){fill[nf]=c;qfill[nf]=q[a][b];nf++;}continue;}
      v[n].n=c;v[n].a=a;v[n].b=b;n++;}
    qsort(v,n,sizeof(Rd),cmp);int bi=-1,bj=-1,best=0;
    for(int i=0;i<n;){int j=i;while(j+1<n&&v[j+1].n*100<=v[j].n*108)j++;if(j-i+1>best&&v[i].n>=50){best=j-i+1;bi=i;bj=j;}i=j+1;}
    if(best==0){continue;}
    long rlo=v[bi].n,rhi=v[bj].n;int small=bi,next=n-1-bj,fl=0;long mf=0,mq=0;
    /* loops below 20x the river are counted with the ordinary roads */
    for(int i=0;i<nf;i++){if(fill[i]>=20*rhi){fl++;if(fill[i]>mf){mf=fill[i];mq=qfill[i];}}else if(fill[i]>rhi)next++;else if(fill[i]<rlo)small++;}
    long qr=q[v[bi].a][v[bi].b];double g=(mf&&mq&&qr)?((double)mf/rhi)/((double)mq/qr):0;
    printf("%s %d %d %d %d %ld %.2f\n",t,small,best,next,fl,rlo,g);}
  return 0;}
