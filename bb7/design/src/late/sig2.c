// Step 3: the oscillator signature, from a blank tape.   Input lines: "S TABLE".
// A machine passes if
//   - it is still running at 10^7 steps,
//   - at 10^6 and at 10^7 steps the tape holds the same row of >= MINROW identical small units (stable fuel),
//   - earlier the row was longer (some units were eaten),
//   - the largest block grew, but slowly: by a factor between 1.5 and 6 for 10x more steps
//     (a machine whose steps cost about block^2 gives 3.2; one that just writes in a line gives 10).
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define TS (1<<22)
static unsigned char t[TS];
static void measure(int lo,int hi,int*row,int*big,int*per){ *row=0;*big=0;*per=0; int c=0;
  for(int i=lo;i<=hi+1;i++){ if(i<=hi&&t[i])c++; else { if(c>*big)*big=c; c=0; } }
  for(int p=2;p<=4;p++) for(int a=lo;a+2*p<=hi+1;a++){ if(!t[a]||t[a-1]||t[a+p-1]) continue; int hz=0; for(int i=0;i<p;i++) if(!t[a+i])hz=1; if(!hz)continue;
      int n=1; while(a+(n+1)*p<=hi+p && !memcmp(t+a,t+a+n*p,p)) n++; if(n>*row){*row=n;*per=p;} a+=(n-1)*p; } }
int main(int argc,char**argv){ int MINROW=atoi(argv[1]); int part=atoi(argv[2]),parts=atoi(argv[3]); char line[128]; char sc; char tm[64]; long n=0;
  int W[7][2],D[7][2],X[7][2],def[7][2];
  while(fgets(line,128,stdin)){ if((n++)%parts!=part) continue; if(sscanf(line,"%c %s",&sc,tm)!=2) continue; memset(def,0,sizeof def);
    for(int s=0;s<7;s++)for(int b=0;b<2;b++){const char*c=tm+s*7+b*3; if(c[0]=='-')continue; def[s][b]=1; W[s][b]=c[0]-'0'; D[s][b]=c[1]=='R'?1:-1; X[s][b]=c[2]-'A';}
    int lo=TS/2,hi=TS/2,pos=TS/2,st=sc-'A'; long s; int end=0; int maxrow=0; int r6=0,b6=0,p6=0,r7=0,b7=0,p7=0;
    for(s=0;s<10000000;s++){
      if(s<200000 && (s&2047)==0){ int r,b,p; measure(lo,hi,&r,&b,&p); if(r>maxrow)maxrow=r; }
      if(s==200000 && maxrow<MINROW+1){end=3;break;}
      if(s==1000000){ measure(lo,hi,&r6,&b6,&p6); if(r6<MINROW||b6<50){end=3;break;} }
      int b=t[pos]; if(!def[st][b]){end=1;break;} t[pos]=W[st][b]; pos+=D[st][b]; st=X[st][b]; if(pos<lo)lo=pos; if(pos>hi)hi=pos; if(pos<8||pos>TS-8){end=2;break;} }
    if(end==1 && s>=1000) { printf("HALT steps=%ld %c %s\n",s,sc,tm); fflush(stdout); }
    else if(end==0){ measure(lo,hi,&r7,&b7,&p7);
      if(r7==r6 && maxrow>r7 && 2*b7>=3*b6 && b7<=6*b6) printf("OSC units=%d (max %d, size %d) big %d->%d %c %s\n",r7,maxrow,p7,b6,b7,sc,tm); fflush(stdout); }
    memset(t+lo-2,0,hi-lo+5); } }
