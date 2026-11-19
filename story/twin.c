/* twin.c T1 T2 STEPS : run two tables side by side from a blank tape; report the first step where head or written symbol differ */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define W 4000000
static char a[W],b[W];int t1[8][2],t2[8][2];
void ld(char*t,int tr[8][2]){int n=(strlen(t)+1)/7;for(int s=0;s<n;s++)for(int x=0;x<2;x++){char*e=t+s*7+x*3;tr[s][x]=(e[2]=='-'||e[2]=='Z')?-1:(e[0]-'0')|((e[1]=='R')<<1)|((e[2]-'A')<<2);}}
int main(int ac,char**av){ld(av[1],t1);ld(av[2],t2);long N=atol(av[3]);long p=W/2,q=W/2;int s=0,u=0;long same=0;
  for(long i=1;i<=N;i++){int e=t1[s][(int)a[p]],f=t2[u][(int)b[q]];
    if(e<0||f<0){printf("step %ld: %s\n",i,e<0&&f<0?"both halt":e<0?"first halts, second goes on":"second halts, first goes on");return 0;}
    if((e&3)!=(f&3)||p!=q){printf("DIFFER at step %ld\n",i);return 0;}
    a[p]=e&1;p+=(e&2)?1:-1;s=e>>2;b[q]=f&1;q+=(f&2)?1:-1;u=f>>2;
    if(p<2||p>W-2){printf("same for %ld steps (tape end)\n",i);return 0;}}
  printf("same tape and head for %ld steps\n",N);return 0;}
