/* hand TABLE RIGHT MAXSTEPS : thought experiment. start in state A on a blank cell with the 0/1 string RIGHT to its right; report halt or the stores at the end */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define W 400000000
static char tape[W];
int main(int ac,char**av){char*t=av[1];char*R=av[2];long max=atol(av[3]);int tr[9][2],n=(strlen(t)+1)/7;
 for(int q=0;q<n;q++)for(int b=0;b<2;b++){char*e=t+q*7+b*3;tr[q][b]=(e[2]=='-'||e[2]=='Z')?-1:(e[0]-'0')|((e[1]=='R')<<1)|((e[2]-'A')<<2);}
 long p=W/2,lo=p,hi=p+strlen(R);for(size_t i=0;i<strlen(R);i++)tape[p+1+i]=R[i]-'0';int s=0;long st=0;
 for(;st<max;st++){int e=tr[s][(int)tape[p]];if(e<0){long ones=0;for(long i=lo;i<=hi;i++)ones+=tape[i];printf("HALT at step %ld, ones %ld (state %c reads %d)\n",st+1,ones+1,'A'+s,tape[p]);return 0;}
   tape[p]=e&1;p+=(e&2)?1:-1;s=e>>2;if(p<lo)lo=p;if(p>hi)hi=p;if(p<8||p>W-8){printf("ran off the tape at step %ld\n",st);return 0;}}
 printf("no halt in %ld steps; stores now:",max);long i=lo;int k=0;while(i<=hi&&k<12){while(i<=hi&&!tape[i])i++;long a=i;while(i<=hi&&tape[i])i++;if(i>a){printf(" %ld",i-a);k++;}}printf("\n");}
