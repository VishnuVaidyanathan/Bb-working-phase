/* search.c "DIGITS" BUDGET          : grow every 7-state table whose run from a blank tape starts with DIGITS, and test each
   search.c -t TABLE                 : run the tests on one table and say what they see
   Digits: A0=0 A1=1 ... G0=c G1=d.  Tables are built only as far as the run needs (as grow.c).
   The tests read only the transcript (the digits), cheapest first:
     test 1  (400 digits)  a ROUND: some digit whose runs get longer by the same amount three times in a row
                           (for example 3x2, 3x5, 3x8).
     test 1b (5,000 digits) the same, four times in a row.
     test 2  a RESET: a later stretch of such growth begins below where an earlier one ended (a block was set down
                           and a new one started).
     test 3  a LAYING: one block of 5 to 40 digits (5 or more different ones) repeated 5 or more times in a row, unchanged,
                           and not just the machine's final loop.
   Prints the tables that pass test 2 (flag R) or tests 2 and 3 (flag RL), with the number of repeats of the laying block.
   Thought tool only. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define TW 801
#define BT 12001
#define NL 5000
int W[14],M[14],X[14],set[14],pre[64],np=0,used=1;
long budget,full=0,halted=0,partial=0,p1=0,p1b=0,p2=0,p3=0,hlate=0;
unsigned char dlog[NL+8];
static int rounds(const unsigned char*d,int n,int need,int*reset){
  /* for each digit: the lengths of its runs, in order.  A round shows as run lengths growing by the same amount:
     L, L+k, L+2k (k>0).  A reset: a later such stretch begins below where an earlier one ended. */
  int p1[14],p2[14],ap[14],best=0,endv[14];*reset=0;
  for(int x=0;x<14;x++){p1[x]=p2[x]=-1;ap[x]=1;endv[x]=-1;}
  for(int i=0;i<n;){int k=i;while(k<n&&d[k]==d[i])k++;
    if(k==n)break;                       /* last run may be cut off by the window */
    int x=d[i],L=k-i;
    if(p1[x]>=0&&L>p1[x]&&(ap[x]==1||L-p1[x]==p1[x]-p2[x])){
      if(ap[x]==1&&endv[x]>=0&&p1[x]<endv[x]&&0){}
      ap[x]++;}
    else{ if(ap[x]>=3){endv[x]=p1[x];} ap[x]=1; }
    if(ap[x]==3&&endv[x]>=0&&p2[x]<endv[x])*reset=1;   /* p2 = first term of this new stretch */
    if(ap[x]>best)best=ap[x];
    p2[x]=p1[x];p1[x]=L;i=k;}
  return best>=need;
}
static int laying(const unsigned char*d,int n){
  int bestr=0;
  for(int p=5;p<=40;p++){int i=0;
    while(i+2*p<=n){int r=1;while(i+(r+1)*p<=n&&!memcmp(d+i,d+i+r*p,p))r++;
      if(r>=5&&i+r*p<n-60){unsigned m=0;for(int k=0;k<p;k++)m|=1u<<d[i+k];if(__builtin_popcount(m)>=5&&r>bestr)bestr=r;}
      i+=(r>1)?(r-1)*p+1:1;}}
  return bestr;
}
void name(char*t){t[0]=0;for(int i=0;i<14;i++){if(!set[i])strcat(t,"1RZ");else sprintf(t+strlen(t),"%d%c%c",W[i],M[i]>0?'R':'L','A'+X[i]);if(i%2&&i<13)strcat(t,"_");}}
static unsigned char big[BT];
void leaf(unsigned char*tape,long pos,int st,long k){
  full++;long off=BT/2-TW/2;memcpy(big+off,tape,TW);pos+=off;long lo=off,hi=off+TW-1;int end=0,rs;
  for(;k<400;k++){int i=st*2+big[pos];if(!set[i]){end=1;break;}dlog[k]=i;big[pos]=W[i];pos+=M[i];st=X[i];if(pos<lo)lo=pos;if(pos>hi)hi=pos;}
  if(!end&&rounds(dlog,400,3,&rs)){p1++;
    for(;k<NL;k++){int i=st*2+big[pos];if(!set[i]){end=1;break;}dlog[k]=i;big[pos]=W[i];pos+=M[i];st=X[i];if(pos<lo)lo=pos;if(pos>hi)hi=pos;}
    if(end)hlate++;
    else if(rounds(dlog,NL,4,&rs)){p1b++;
      if(rs){p2++;int r=laying(dlog,NL);char t[120];name(t);
        if(r){p3++;printf("RL %d %s\n",r,t);}else printf("R 0 %s\n",t);}}}
  else if(end)halted++;
  memset(big+lo-1,0,hi-lo+3);
}
void go(unsigned char*tape,long pos,int st,long k,int nset){
  for(;;){
    int i=st*2+tape[pos];
    if(k<np&&i!=pre[k])return;
    if(nset==13&&k>=np){leaf(tape,pos,st,k);return;}
    if(k>=budget){partial++;return;}
    if(!set[i]){
      unsigned char cp[TW];int u0=used;
      for(int x=0;x<=used&&x<7;x++)for(int w=0;w<2;w++)for(int m=-1;m<2;m+=2){
        if(k+1<np&&x!=pre[k+1]/2)continue;
        W[i]=w;M[i]=m;X[i]=x;set[i]=1;if(x==used)used++;
        memcpy(cp,tape,TW);cp[pos]=w;dlog[k]=i;go(cp,pos+m,x,k+1,nset+1);
        set[i]=0;used=u0;}
      return;}
    dlog[k]=i;tape[pos]=W[i];pos+=M[i];st=X[i];k++;
    if(pos<1||pos>TW-2){partial++;return;}
  }
}
int main(int c,char**v){
  if(!strcmp(v[1],"-t")){char*t=v[2];for(int q=0;q<7;q++)for(int b=0;b<2;b++){char*e=t+q*7+b*3;int i=q*2+b;if(e[2]=='Z'||e[2]=='-')set[i]=0;else{set[i]=1;W[i]=e[0]-'0';M[i]=e[1]=='R'?1:-1;X[i]=e[2]-'A';}}
    long pos=BT/2;int st=0,k,rs,rs2;for(k=0;k<NL;k++){int i=st*2+big[pos];if(!set[i])break;dlog[k]=i;big[pos]=W[i];pos+=M[i];st=X[i];}
    if(k<NL){printf("%s halts at step %d\n",t,k);return 0;}
    int a=rounds(dlog,400,3,&rs),b=rounds(dlog,NL,4,&rs2);
    printf("%s | test 1: %s | test 1b: %s | test 2 (reset): %s | test 3 (laying): %d repeats\n",t,a?"pass":"fail",b?"pass":"fail",rs2?"pass":"fail",laying(dlog,NL));return 0;}
  for(char*p=v[1];*p;p++){if(*p==' ')continue;pre[np++]=(*p>='a')?*p-'a'+10:*p-'0';}
  budget=atol(v[2]);unsigned char tape[TW];memset(tape,0,TW);go(tape,TW/2,0,0,0);
  fprintf(stderr,"%s | full tables %ld | halt in 400 steps %ld | test 1 pass %ld | (halt by 5,000: %ld) | test 1b pass %ld | test 2 pass %ld | test 3 pass %ld | open after budget %ld\n",v[1],full,halted,p1,hlate,p1b,p2,p3,partial);}
