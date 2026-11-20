/* layer TABLE STATE K : start on the tape  [0](10)^K 1111  in STATE, head on the blank cell just left of the stripes;
   run until the head is again left of everything on a tape of the same form; print next K, the state there, steps, and how often road b>3 was used */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define W 60000000
static char tape[W];
int main(int ac,char**av){char*t=av[1];int s=av[2][0]-'A';long K=atol(av[3]);int tr[8][2],n=(strlen(t)+1)/7;
 for(int q=0;q<n;q++)for(int b=0;b<2;b++){char*e=t+q*7+b*3;tr[q][b]=(e[2]=='-'||e[2]=='Z')?-1:(e[0]-'0')|((e[1]=='R')<<1)|((e[2]-'A')<<2);}
 long p=W/2,lo,hi;for(long i=0;i<K;i++)tape[p+1+2*i]=1;for(int i=0;i<4;i++)tape[p+1+2*K+i]=1;lo=p+1;hi=p+2*K+4;
 long ones=K+4;int prev=-1;long b3=0,st=0,maxsteps=ac>4?atol(av[4]):400000000000L;
 for(;;st++){int d=2*s+tape[p];if(prev==11&&d==3)b3++;
   if(st>0&&p<lo&&tape[p]==0){ /* left of everything: is the tape stripes + 1111 ? */
     long len=hi-lo+1;if(len>=4&&(len%2)==0&&ones==(len-4)/2+4){int ok=1;long kk=(len-4)/2;
       for(long i=0;i<kk&&ok;i++)if(!(tape[lo+2*i]==1&&tape[lo+2*i+1]==0))ok=0;
       for(int i=0;i<4&&ok;i++)if(!tape[hi-i])ok=0;
       if(ok&&p==lo-1){printf("K=%ld start=%s -> K=%ld state=%c steps=%ld b3=%ld\n",K,av[2],kk,'A'+s,st,b3);return 0;}}}
   int e=tr[s][(int)tape[p]];if(e<0){printf("K=%ld start=%s -> HALT steps=%ld\n",K,av[2],st);return 0;}
   if(st>=maxsteps){printf("K=%ld start=%s -> not finished in %ld steps\n",K,av[2],st);return 0;}
   prev=d;ones+=(e&1)-tape[p];tape[p]=e&1;if((e&1)){if(p<lo)lo=p;if(p>hi)hi=p;}
   else{ if(p==lo){while(lo<=hi&&!tape[lo])lo++;} if(p==hi){while(hi>=lo&&!tape[hi])hi--;} }
   p+=(e&2)?1:-1;s=e>>2;}
}
