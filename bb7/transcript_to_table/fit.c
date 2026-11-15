// "Which tables support this?"  Next states are fixed (roles); writes and moves are free.
// Each table is run from a blank tape; a wire is filled only when the run reaches it.
// We ask: does the run reach the gate tape   1 0 [G reads 0] 1^P 0^g 1 <end>   (P >= PMIN)?
// usage: fit ROLES CAP PMIN      e.g. fit BGCBD?EDFEAFCB 3000 5
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define W 65536
typedef struct { unsigned char tape[W]; int p,s,lo,hi; long t; } Cfg;
static int nx[7][2], wr[7][2], mv[7][2], def[7][2]; static long CAP; static int PMIN; static long ntab=0,nhit=0;
static void emit(int P,int g,long t,int clean){ char b[64]; int k=0; for(int s=0;s<7;s++){ for(int r=0;r<2;r++){ if(!def[s][r]){b[k++]='-';b[k++]='-';b[k++]='-';} else {b[k++]='0'+wr[s][r];b[k++]=mv[s][r]>0?'R':'L';b[k++]='A'+nx[s][r];} } if(s<6)b[k++]='_'; } b[k]=0; printf("P=%d g=%d t=%ld clean=%d %s\n",P,g,t,clean,b); nhit++; }
static void run(Cfg*c){
  for(;;){ if(c->t>=CAP){ntab++;return;} int r=c->tape[c->p]; int s=c->s;
    if(s==6&&r==0&&c->t>0){ int hi=c->hi; while(hi>c->p&&!c->tape[hi])hi--; int i=c->p+1,a=0,g=0; while(i<=hi&&c->tape[i]){a++;i++;} while(i<=hi&&!c->tape[i]){g++;i++;}
      if(a>=PMIN&&g>=1&&i==hi){ int clean=(c->tape[c->p-1]==0&&c->tape[c->p-2]==1); emit(a,g,c->t,clean); ntab++; return; } }
    if(nx[s][r]<0){ntab++;return;}            // halt wire
    if(!def[s][r]){ Cfg*d=malloc(sizeof(Cfg)); for(int w=0;w<2;w++)for(int m=-1;m<=1;m+=2){ if(c->t==0&&m<0)continue; def[s][r]=1;wr[s][r]=w;mv[s][r]=m; memcpy(d,c,sizeof(Cfg)); run(d);} def[s][r]=0; free(d); return; }
    c->tape[c->p]=wr[s][r]; c->p+=mv[s][r]; c->s=nx[s][r]; c->t++; if(c->p<c->lo)c->lo=c->p; if(c->p>c->hi)c->hi=c->p; if(c->p<4||c->p>W-4){ntab++;return;} } }
int main(int n,char**v){ const char*ro=v[1]; CAP=atol(v[2]); PMIN=atoi(v[3]); for(int s=0;s<7;s++)for(int r=0;r<2;r++){ char ch=ro[2*s+r]; nx[s][r]=(ch=='?')?-1:ch-'A'; }
  Cfg*c=calloc(1,sizeof(Cfg)); c->p=c->lo=c->hi=W/2; run(c); fprintf(stderr,"tables %ld hits %ld\n",ntab,nhit); }
