// "Convert the grammar into wiring", tested on BB(5).
// The grammar of the champion's transcript fixes WHO FOLLOWS WHOM:
//   pairs 02, 46      : A0 -> B,  B0 -> C,  C0 -> D,  D0 -> A
//   oscillator 1 5 9  : A1 -> C,  C1 -> E,  E1 -> A
//   fillers 7, 3      : D1 -> D,  B1 -> B
//   halt 8            : E0
// What the grammar does NOT fix is what each wire writes and which way it moves: 4 choices for each of 9 wires.
// This program tries all 4^9 = 262,144 tables with that skeleton, from a blank tape.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define TS (1<<17)
static unsigned char t[TS];
int NX[5][2]={{1,2},{2,1},{3,4},{0,3},{5,0}};
int main(int argc,char**argv){ long L1=atol(argv[1]), L2=atol(argv[2]); long nh=0,nrun=0,nlin=0,nsmall=0;
  for(int code=0;code<262144;code++){ int W[5][2],D[5][2]; int c=code;
    for(int s=0;s<5;s++)for(int b=0;b<2;b++){ if(s==4&&b==0)continue; W[s][b]=c&1; D[s][b]=(c&2)?1:-1; c>>=2; }
    if(D[0][0]!=1) continue;                 // first move to the right (the mirror image is the same machine)
    int pos=TS/2,st=0,lo=pos,hi=pos; long s; int halted=0,edge=0; long lim=L1;
    for(s=0;s<lim;s++){ int b=t[pos]; if(st==4&&b==0){halted=1;break;}
      t[pos]=W[st][b]; pos+=D[st][b]; st=NX[st][b]; if(pos<lo)lo=pos; if(pos>hi)hi=pos; if(pos<4||pos>TS-4){edge=1;break;}
      if(s==L1-1){ int w=hi-lo; if(w>6000){nlin++;break;} if(w<12){nsmall++;break;} lim=L2; } }
    if(halted){ nh++; if(s>=1000){ long ones=0; for(int i=lo;i<=hi;i++)ones+=t[i]; char buf[40]; int k=0;
        for(int q=0;q<5;q++){ for(int b=0;b<2;b++){ if(q==4&&b==0){buf[k++]='-';buf[k++]='-';buf[k++]='-';} else {buf[k++]='0'+W[q][b];buf[k++]=D[q][b]>0?'R':'L';buf[k++]='A'+NX[q][b];} } buf[k++]='_'; } buf[k-1]=0;
        printf("%ld %ld %s\n",s+1,ones,buf); } }
    else if(!edge && s>=L2) nrun++;
    memset(t+lo-1,0,hi-lo+3); }
  fprintf(stderr,"halting: %ld   still running at the limit: %ld   run off in a line: %ld   stuck in a small area: %ld\n",nh,nrun,nlin,nsmall); }
