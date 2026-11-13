// The micro-structure of the champion's run from a blank tape.
// For every step: which wire acts, which wire acts next (the branch), and which wire had written the cell it reads.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define TS (1<<24)
static unsigned char t[TS], who[TS];   // who[cell] = 1 + wire that last wrote it, 0 = never written (blank)
int main(int argc,char**argv){ long N=atol(argv[1]); const char*tm="1RB0RG_1RC1RB_0RD1RZ_0LE0LD_0LF1LE_1RA1LF_1LC0RB";
  int W[7][2],D[7][2],X[7][2];
  for(int s=0;s<7;s++)for(int b=0;b<2;b++){const char*c=tm+s*7+b*3; W[s][b]=c[0]-'0'; D[s][b]=c[1]=='R'?1:-1; X[s][b]=c[2]=='Z'?7:c[2]-'A';}
  static long use[14], next[14][15], wr[15][14], flip[14];
  int pos=TS/2,st=0; int prev=-1; long s;
  for(s=0;s<N&&st!=7;s++){ int b=t[pos]; int w=2*st+b; use[w]++; if(prev>=0) next[prev][w]++; wr[who[pos]][w]++;
    if(W[st][b]!=b) flip[w]++;
    t[pos]=W[st][b]; who[pos]=1+w; pos+=D[st][b]; st=X[st][b]; prev=w; }
  const char*nm[14]={"A0","A1","B0","B1","C0","C1","D0","D1","E0","E1","F0","F1","G0","G1"};
  printf("steps %ld\n\nwire   uses        changes the cell   then goes to (share)\n",s);
  for(int w=0;w<14;w++){ if(!use[w]){printf("%s   never used\n",nm[w]);continue;} printf("%s  %10ld   %5.1f%%            ",nm[w],use[w],100.0*flip[w]/use[w]);
    for(int v=0;v<14;v++) if(next[w][v]) printf("%s %.4g%%  ",nm[v],100.0*next[w][v]/use[w]); printf("\n"); }
  printf("\nwho wrote the cell that each wire reads (share of that wire's reads)\nreader:  ");
  for(int w=0;w<14;w++) if(use[w]) printf("%s: ",nm[w]), 0; printf("\n");
  for(int w=0;w<14;w++){ if(!use[w])continue; printf("%s reads cells written by: ",nm[w]);
    for(int a=0;a<15;a++) if(wr[a][w]*1000>=use[w]) printf("%s %.3g%%  ",a?nm[a-1]:"blank",100.0*wr[a][w]/use[w]); printf("\n"); } }
