/* life7 TABLE MAXSTEPS : run from a blank tape; each time the machine is at rest (state A on a blank cell with nothing to its left)
   and the tape is a fresh row (every block the same small size), print it; at the end print the stores. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define W 200000000
static char tape[W];
int main(int ac,char**av){char*t=av[1];long max=atol(av[2]);int tr[8][2],n=(strlen(t)+1)/7;
 for(int q=0;q<n;q++)for(int b=0;b<2;b++){char*e=t+q*7+b*3;tr[q][b]=(e[2]=='-'||e[2]=='Z')?-1:(e[0]-'0')|((e[1]=='R')<<1)|((e[2]-'A')<<2);}
 long p=W/2,lo=p,hi=p,st=0;int s=0;long lastrow=-1;
 for(;st<max;st++){
   if(s==0&&tape[p]==0&&p<=lo){ /* at rest at the far left */
     long i=p+1,cnt=0,size=-1;int ok=1;long h=hi;while(h>p&&!tape[h])h--;
     while(i<=h&&ok){long a=i;while(i<=h&&tape[i])i++;long len=i-a;if(len==0){ok=0;break;}if(size<0)size=len;else if(len!=size&&i<=h)ok=0;else if(len!=size&&i>h&&cnt<1)ok=0;cnt++;if(i<=h){if(tape[i+1]==0&&i+1<=h){ok=0;}i++;}}
     if(ok&&cnt>=2&&size<=3&&cnt!=lastrow){printf("step %ld: fresh row of %ld stores of size %ld\n",st,cnt,size);lastrow=cnt;}
   }
   int e=tr[s][(int)tape[p]];if(e<0){long ones=0;for(long i=lo;i<=hi;i++)ones+=tape[i];printf("HALT at step %ld, ones %ld (state %c reads %d)\n",st+1,ones+1,'A'+s,tape[p]);return 0;}
   tape[p]=e&1;p+=(e&2)?1:-1;s=e>>2;if(p<lo)lo=p;if(p>hi)hi=p;}
 printf("no halt in %ld steps; stores now:",max);long i=lo;int k=0;while(i<=hi&&k<14){while(i<=hi&&!tape[i])i++;long a=i;while(i<=hi&&tape[i])i++;if(i>a){printf(" %ld",i-a);k++;}}printf("\n");}
