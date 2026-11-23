/* cls.c BUDGET : every 7-state table that "looks the same in the transcript" as the grammar Vishnu read (23 Nov):
     - the even digits make one closed loop A0->B0->C0->D0->E0->F0->A (A0 = 1RB; the others write 0/1, move L/R);
     - the odd halves of the six loop states are: three fillers (write 1, L or R, point to their own state),
       one take (write 0, L or R, points to its own state), one door (any write/move, goes to G), one halt - in any arrangement;
     - G is only behind the door; G0 and G1: any write/move, back to any loop state.
   Tables are built only as far as a run from a blank tape needs them (a wire is chosen when the head first reads it),
   so tables that behave the same are not repeated.  BUDGET = steps allowed while wires are still open.
   Output: full tables (all 13 wires chosen) on stdout; counts on stderr.  Thought tool only. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define TW 20001
int W[14],M[14],X[14],set[14];   /* X: 0..6 state, -1 halt */
int nfill=3,ntake=1,ndoor=1,nhalt=1;
long budget,full=0,halted=0,partial=0,nodes=0;
void emit(){char t[120]="";for(int i=0;i<14;i++){if(!set[i])strcat(t,"---");else if(X[i]<0)strcat(t,"1RZ");else sprintf(t+strlen(t),"%d%c%c",W[i],M[i]>0?'R':'L','A'+X[i]);if(i%2&&i<13)strcat(t,"_");}puts(t);}
void go(unsigned char*tape,long pos,int st,long k,int nset){
  nodes++;
  for(;;){
    if(k>=budget){partial++;return;}
    int i=st*2+tape[pos];
    if(!set[i]){
      unsigned char*cp=malloc(TW);
      #define TRY(w,m,x) {W[i]=w;M[i]=m;X[i]=x;set[i]=1;memcpy(cp,tape,TW);go(cp,pos,st,k,nset+1);set[i]=0;}
      if(st==6){for(int w=0;w<2;w++)for(int m=-1;m<2;m+=2)for(int x=0;x<6;x++)TRY(w,m,x)}
      else if(!(i&1)){for(int w=0;w<2;w++)for(int m=-1;m<2;m+=2)TRY(w,m,(st+1)%6)}
      else{
        if(nfill){nfill--;TRY(1,-1,st)TRY(1,1,st)nfill++;}
        if(ntake){ntake--;TRY(0,-1,st)TRY(0,1,st)ntake++;}
        if(ndoor){ndoor--;for(int w=0;w<2;w++)for(int m=-1;m<2;m+=2)TRY(w,m,6)ndoor++;}
        if(nhalt){nhalt--;W[i]=1;M[i]=1;X[i]=-1;set[i]=1;halted++;set[i]=0;nhalt++;}
      }
      free(cp);return;
    }
    if(X[i]<0){halted++;return;}
    tape[pos]=W[i];pos+=M[i];st=X[i];k++;
    if(pos<1||pos>TW-2){partial++;return;}
    if(nset==13){   /* every wire that can act is chosen; the one left is the halt */
      int h=-1;for(int j=1;j<12;j+=2)if(!set[j])h=j;X[h]=-1;W[h]=1;M[h]=1;set[h]=1;emit();set[h]=0;
      full++;return;}
  }
}
int main(int c,char**v){budget=atol(v[1]);unsigned char*tape=calloc(TW,1);
  W[0]=1;M[0]=1;X[0]=1;set[0]=1;go(tape,TW/2,0,0,1);
  fprintf(stderr,"full tables: %ld | halted while wires were still open: %ld | still open after the budget: %ld | nodes %ld\n",full,halted,partial,nodes);}
