/* riverc.c STEPS : reads tables (first word of each line), runs each from a blank tape, and prints
   table, river size (the most roads used about equally often, within 12 percent, not counting loops), how often the river
   runs, and the number of idle digits (used less than 5 percent as often as the river). */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define W 400000
static char tape[W];
static int cmp(const void*a,const void*b){long x=*(long*)a,y=*(long*)b;return x<y?-1:x>y;}
int main(int ac,char**av){long NS=atol(av[1]);char line[4096];
  while(fgets(line,4096,stdin)){char t[64];if(sscanf(line,"%60s",t)!=1||strlen(t)<48)continue;int tr[7][2];
    for(int s=0;s<7;s++)for(int b=0;b<2;b++){char*e=t+s*7+b*3;tr[s][b]=(e[2]=='-'||e[2]=='Z')?-1:(e[0]-'0')|((e[1]=='R')<<1)|((e[2]-'A')<<2);}
    memset(tape,0,W);long p=W/2;int s=0,prev=-1;static long pc[14][14];long dc[14];memset(pc,0,sizeof(pc));memset(dc,0,sizeof(dc));
    for(long n=0;n<NS;n++){int b=tape[p],d=2*s+b;dc[d]++;if(prev>=0)pc[prev][d]++;prev=d;int e=tr[s][b];if(e<0)break;tape[p]=e&1;p+=(e&2)?1:-1;s=e>>2;if(p<5||p>W-5)break;}
    long v[200];int n=0;
    for(int a=0;a<14;a++)for(int b=0;b<14;b++){if(!pc[a][b]||a==b)continue;if(pc[b][a]*10>pc[a][b]*8&&pc[a][b]*10>pc[b][a]*8&&pc[a][b]>20*1000)continue;v[n++]=pc[a][b];}
    qsort(v,n,sizeof(long),cmp);int best=0;long bl=0;
    for(int i=0;i<n;i++){if(v[i]<50)continue;int j=i;while(j+1<n&&v[j+1]*100<=v[i]*112)j++;if(j-i+1>best){best=j-i+1;bl=v[i];}}
    int idle=0,used=0;for(int d=0;d<14;d++){if(dc[d]){used++;if(dc[d]*20<bl)idle++;}}
    printf("%s %d %ld %d %d\n",t,best,bl,idle,used);}
  return 0;}
