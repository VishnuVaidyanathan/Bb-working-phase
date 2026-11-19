/* flow.c WIRING BUDGET : the wiring is fixed first (which state each of the 14 digits flows to), then every choice of
   "write 0/1, move left/right" is tried from a blank tape, but only as far as the run needs it.
   WIRING = 14 letters, the next state for digits 0 1 2 ... d  (Z = the halt).  Jeff's is BGCBDZEDFEAFCB.
   For every run still alive at BUDGET steps it prints the table and its road counts (also at a quarter of the budget). */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define W 30000
int nxt[14],tr[7][2];long BUD;
typedef struct{char t[W];int p,s,prev,lo,hi;long steps;int pc[14][14],q[14][14];}Sim;
static void name(char*b){int k=0;for(int s=0;s<7;s++){for(int x=0;x<2;x++){int e=tr[s][x];if(nxt[2*s+x]<0){b[k++]='1';b[k++]='R';b[k++]='Z';}else if(e<0){b[k++]='-';b[k++]='-';b[k++]='-';}else{b[k++]='0'+(e&1);b[k++]=(e&2)?'R':'L';b[k++]='A'+nxt[2*s+x];}}if(s<6)b[k++]='_';}b[k]=0;}
static void rec(Sim*S){
  long wins=S->steps;int wlo=S->p,whi=S->p;
  for(;;){
    int b=S->t[S->p],d=2*S->s+b;
    if(S->prev>=0)S->pc[S->prev][d]++;
    S->prev=d;
    if(nxt[d]<0)return;                       /* reached the halt inside the budget: too small, drop */
    int e=tr[S->s][b];
    if(e<0){for(int c=0;c<4;c++){tr[S->s][b]=c;Sim*C=malloc(sizeof(Sim));memcpy(C,S,sizeof(Sim));C->pc[C->prev][d]+=0;
        /* undo the count of this visit in the copy: it will be counted again */ if(0){}
        C->prev=S->prev; rec2:; 
        {int bb=C->t[C->p];int ee=c;C->t[C->p]=ee&1;C->p+=(ee&2)?1:-1;C->s=nxt[d];C->steps++;if(C->p<C->lo)C->lo=C->p;if(C->p>C->hi)C->hi=C->p;(void)bb;}
        if(C->p>40&&C->p<W-40)rec(C);free(C);tr[S->s][b]=-1;}
      return;}
    S->t[S->p]=e&1;S->p+=(e&2)?1:-1;S->s=nxt[d];S->steps++;
    if(S->p<S->lo)S->lo=S->p;if(S->p>S->hi)S->hi=S->p;
    if(S->p<wlo)wlo=S->p;if(S->p>whi)whi=S->p;
    if(S->steps-wins>=3000){if(whi-wlo<10)return;wlo=whi=S->p;wins=S->steps;}
    if(S->p<=40||S->p>=W-40)return;
    if(S->steps==BUD/4)memcpy(S->q,S->pc,sizeof(S->pc));
    if(S->steps>=BUD){char nm[80];name(nm);printf("%s %d",nm,S->hi-S->lo);
      for(int a=0;a<14;a++){int k0=nxt[a]<0?-1:2*nxt[a];if(k0<0){printf(" 0 0 0 0");continue;}printf(" %d %d %d %d",S->pc[a][k0],S->pc[a][k0+1],S->q[a][k0],S->q[a][k0+1]);}
      printf("\n");return;}
  }}
int main(int ac,char**av){for(int i=0;i<14;i++)nxt[i]=av[1][i]=='Z'?-1:av[1][i]-'A';BUD=atol(av[2]);
  for(int s=0;s<7;s++)tr[s][0]=tr[s][1]=-1;Sim*S=calloc(1,sizeof(Sim));S->p=W/2;S->lo=S->hi=W/2;S->prev=-1;
  tr[0][0]=3; /* first step: write 1, move right (the usual normal form) */
  rec(S);return 0;}
