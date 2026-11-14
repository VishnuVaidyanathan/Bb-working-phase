// n-gram Closed Position Set (after Nathan Fenner / savask / Skelet): a sound proof that a machine never halts.
// Keep: the set of n-cell words seen left of the head, the same for the right, and the set of local pictures
// (left n cells, state, cell under head, right n cells). Close the sets under the machine's moves.
// If the closure never touches the empty wire, the machine cannot halt.
// usage: ncps NMAX MAXCTX < lines ending with a table ; prints "N n table" (proved non-halting with window n) or "U table".
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
int NS,W[8][2],D[8][2],X[8][2],def[8][2];
#define HB 22
static uint64_t ht[1<<HB]; static uint64_t *lst; static unsigned char *LG,*RG; long nc,MAXC;
int add(uint64_t k){ uint64_t h=(k*0x9E3779B97F4A7C15ULL)>>(64-HB); while(ht[h]){ if(ht[h]==k+1) return 0; h=(h+1)&((1<<HB)-1);} ht[h]=k+1; lst[nc++]=k; return 1; }
int cps(int n){ uint64_t mask=(1ULL<<n)-1; memset(ht,0,sizeof ht); memset(LG,0,1<<n); memset(RG,0,1<<n); nc=0; LG[0]=RG[0]=1;
  add(0); // l=0,r=0,h=0,st=0
  int ch=1; while(ch){ ch=0;
    for(long i=0;i<nc;i++){ uint64_t k=lst[i]; uint64_t l=k&mask, r=(k>>n)&mask; int h=(k>>(2*n))&1, st=k>>(2*n+1);
      if(!def[st][h]) return 0;
      int w=W[st][h], s2=X[st][h];
      if(D[st][h]>0){ if(!LG[l]){LG[l]=1;ch=1;} uint64_t l2=((l<<1)|w)&mask; int h2=r&1;
        for(uint64_t c=0;c<2;c++){ uint64_t r2=(r>>1)|(c<<(n-1)); if(!RG[r2]) continue;
          if(add(l2|(r2<<n)|((uint64_t)h2<<(2*n))|((uint64_t)s2<<(2*n+1)))){ch=1; if(nc>=MAXC) return 0;} } }
      else { if(!RG[r]){RG[r]=1;ch=1;} uint64_t r2=((r<<1)|w)&mask; int h2=l&1;
        for(uint64_t c=0;c<2;c++){ uint64_t l2=(l>>1)|(c<<(n-1)); if(!LG[l2]) continue;
          if(add(l2|(r2<<n)|((uint64_t)h2<<(2*n))|((uint64_t)s2<<(2*n+1)))){ch=1; if(nc>=MAXC) return 0;} } } } }
  return 1; }
int main(int argc,char**argv){ int NMAX=atoi(argv[1]); MAXC=atol(argv[2]); lst=malloc(8*(MAXC+4)); LG=malloc(1<<NMAX); RG=malloc(1<<NMAX);
  char line[256]; while(fgets(line,256,stdin)){ char*tm=strrchr(line,' '); tm=tm?tm+1:line; tm[strcspn(tm,"\n")]=0; NS=(strlen(tm)+1)/7; memset(def,0,sizeof def);
    for(int s=0;s<NS;s++)for(int b=0;b<2;b++){const char*c=tm+s*7+b*3; if(c[0]=='-'||c[2]=='Z')continue; def[s][b]=1; W[s][b]=c[0]-'0'; D[s][b]=c[1]=='R'?1:-1; X[s][b]=c[2]-'A';}
    int ok=0; for(int n=1;n<=NMAX;n++) if(cps(n)){ok=n;break;}
    if(ok) printf("N %d %s\n",ok,tm); else printf("U %s\n",tm); fflush(stdout); } }
