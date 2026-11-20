/* jexp TABLE STATE LEFT RIGHT MAXSTEPS MAXEVENTS : run TABLE from a hand-made tape (head on first cell of RIGHT) and, each time digit c is read
   straight after digit 1, print the tape as: left part verbatim | runs of ones to the right as  n.g  (n ones then g zeros), pieces 1100 counted */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define W 400000000
static char tape[W];
int main(int ac,char**av){char*t=av[1];int s=av[2][0]-'A';char*L=av[3],*R=av[4];long max=atol(av[5]);int maxev=atoi(av[6]);int tr[8][2],n=(strlen(t)+1)/7;
 for(int q=0;q<n;q++)for(int b=0;b<2;b++){char*e=t+q*7+b*3;tr[q][b]=(e[2]=='-'||e[2]=='Z')?-1:(e[0]-'0')|((e[1]=='R')<<1)|((e[2]-'A')<<2);}
 long p=W/2,lo=p-strlen(L),hi=p+strlen(R)-1;for(size_t i=0;i<strlen(L);i++)tape[lo+i]=L[i]-'0';for(size_t i=0;i<strlen(R);i++)tape[p+i]=R[i]-'0';
 int prev=-1,ev=0;
 for(long st=0;st<max;st++){int d=2*s+tape[p];
   if((prev==1&&d==12)||(prev==13&&d==2)){ while(lo<p&&!tape[lo])lo++; while(hi>p&&!tape[hi])hi--;
     printf("%11ld %s  ",st,d==12?"1c":"d2");for(long i=lo;i<p;i++)putchar('0'+tape[i]);printf("[%d] ",tape[p]);
     long i=p+1;int pieces=0,out=0;
     while(i<=hi&&out<14){long a=i;while(i<=hi&&tape[i])i++;long b=i;while(i<=hi&&!tape[i])i++;
        if(b-a==2&&i-b==2){pieces++;continue;}
        if(pieces){printf("(1100)x%d ",pieces);pieces=0;}
        if(b>a)printf("%ld.%ld ",b-a,i-b);else printf("_.%ld ",i-b);out++;}
     if(pieces)printf("(1100)x%d ",pieces);
     printf("\n");if(++ev>=maxev)return 0;}
   int e=tr[s][(int)tape[p]];if(e<0){long ones=0;for(long i=lo;i<=hi;i++)ones+=tape[i];printf("HALT at step %ld, ones %ld\n",st+1,ones+1);return 0;}
   prev=d;tape[p]=e&1;p+=(e&2)?1:-1;s=e>>2;if(p<lo)lo=p;if(p>hi)hi=p;}
 printf("no halt in %ld steps\n",max);}
