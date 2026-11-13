// Step 1 of the engineering pipeline: "take the block apart and pack it into units".
// Seed: an up-stroke loop with a door.  Tape: [A] 0^g 1^P (blank elsewhere).  The seed first turns this into
// one solid block Q.  We then add <= ADD wires (lazily) so that later the tape holds a row of at least
// Q/2 - 3 identical small units (period 2, 3 or 4 cells, e.g. "10", "110", "1100"), with no more ones than Q + 4.
// Checked for P = 4 and P = 6; the row must be longer for P = 6.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
int ADD=4, G; int W[7][2], D[7][2], X[7][2], def[7][2]; int nw, nw0; long nodes=0, found=0; char seed[64];
#define TS 1024
int ust,usym,rRow,rPer,rQ;
int runtest(int P){
  static unsigned char t[TS]; memset(t,0,TS); int base=500; for(int i=0;i<P;i++)t[base+G+i]=1;
  int pos=base, st=0, ones=P, lo=base-300, hi=base+300; int Q=0; int l1=base+G,r1=base+G+P-1;
  for(int s=0;s<30000;s++){
    int b=t[pos]; if(!def[st][b]){ust=st;usym=b;return -2;}
    int w=W[st][b]; ones+=w-b; t[pos]=w; if(w){ if(pos<l1)l1=pos; if(pos>r1)r1=pos; } pos+=D[st][b]; st=X[st][b];
    if(pos<lo||pos>hi||ones==0) return -1;
    if((s&7)==0){ while(l1<r1&&!t[l1])l1++; while(r1>l1&&!t[r1])r1--;
      if(ones==r1-l1+1 && ones>=2*P && ones>Q) Q=ones;
      if(Q && ones<=Q+4 && ones>=Q/2){
        for(int per=3;per<=4;per++){ int best=0, bu=0;
          for(int a=l1;a+2*per<=r1+1;a++){ if(!t[a]||t[a-1]) continue; int hasz=0; for(int i=0;i<per;i++) if(!t[a+i]) hasz=1; if(!hasz||t[a+per-1]) continue;
            int n=1; while(a+(n+1)*per<=r1+per && !memcmp(t+a,t+a+n*per,per)) n++; if(n>best){best=n; int u=0; for(int i=0;i<per;i++)u+=t[a+i]; bu=u;} }
          if(best>=4 && best*bu*10>=7*ones && ones*10>=7*Q){ rRow=best; rPer=per; rQ=Q; return 1; } } } }
  }
  return -1;
}
void name(char*buf){int k=0; for(int s=0;s<7;s++){ for(int b=0;b<2;b++){ if(def[s][b]){buf[k++]='0'+W[s][b];buf[k++]=D[s][b]>0?'R':'L';buf[k++]='A'+X[s][b];} else {buf[k++]='-';buf[k++]='-';buf[k++]='-';} } buf[k++]='_';} buf[k-1]=0;}
void dfs(void){ nodes++;
  int r=runtest(4); if(r==-1) return;
  if(r==1){ int row4=rRow,per4=rPer,q4=rQ; r=runtest(6); if(r==-1) return;
    if(r==1){ if(rRow>row4 && rPer==per4 && nw>nw0){ char buf[64]; name(buf); found++; printf("PACK g=%d add=%d wires=%d unit=%d top=%d,%d row=%d,%d %s\n",G,nw-nw0,nw,rPer,q4,rQ,row4,rRow,buf);} return; } }
  if(nw-nw0>=ADD) return;
  int s=ust,b=usym; def[s][b]=1; nw++;
  for(int nx=0;nx<7;nx++) for(int w=0;w<2;w++) for(int d=-1;d<=1;d+=2){ W[s][b]=w;D[s][b]=d;X[s][b]=nx; dfs(); }
  def[s][b]=0; nw--; }
int main(int argc,char**argv){ ADD=atoi(argv[1]); int part=atoi(argv[2]),parts=atoi(argv[3]); char line[256]; long n=0;
  while(fgets(line,256,stdin)){ if((n++)%parts!=part) continue; char*p=strstr(line,"g="); if(!p)continue; G=atoi(p+2);
    char*q=strrchr(line,' '); strcpy(seed,q+1); seed[strcspn(seed,"\n")]=0; memset(def,0,sizeof def); nw=0;
    for(int s=0;s<7;s++)for(int b=0;b<2;b++){ if(strlen(seed)<(size_t)(s*7+b*3+3)) continue; const char*c=seed+s*7+b*3; if(c[0]=='-')continue; def[s][b]=1; nw++; W[s][b]=c[0]-'0'; D[s][b]=c[1]=='R'?1:-1; X[s][b]=c[2]-'A';}
    nw0=nw; dfs(); }
  fprintf(stderr,"ADD=%d nodes=%ld found=%ld\n",ADD,nodes,found); }
