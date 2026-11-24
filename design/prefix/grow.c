/* grow.c "DIGITS" BUDGET [print] : every 7-state table whose run from a blank tape starts with the given digits
   (0-9 a-d, spaces ignored; A0=0 A1=1 ... G1=d).  Tables are built only as far as the run needs: a wire is chosen when the
   head first reads it (any write, any move; next state = a state already used or the next unused one).  Exactly one wire is
   left as the halt: a table is full when 13 wires are chosen.  BUDGET = steps allowed while wires are still open.
   Prints counts; with "print" also the full tables.  Thought tool only. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define TW 4001
int W[14],M[14],X[14],set[14],pre[64],np=0,doprint=0,used=1;
long budget,full=0,halted=0,partial=0,mism=0;
void emit(){char t[120]="";for(int i=0;i<14;i++){if(!set[i])strcat(t,"1RZ");else sprintf(t+strlen(t),"%d%c%c",W[i],M[i]>0?'R':'L','A'+X[i]);if(i%2&&i<13)strcat(t,"_");}puts(t);}
void go(unsigned char*tape,long pos,int st,long k,int nset){
  for(;;){
    int i=st*2+tape[pos];
    if(k<np&&i!=pre[k]){mism++;return;}
    if(nset==13&&k>=np){full++;if(doprint)emit();return;}
    if(k>=budget){partial++;return;}
    if(!set[i]){
      if(nset==13){halted++;return;}      /* the last open wire is the halt */
      unsigned char cp[TW];int u0=used;
      for(int x=0;x<=used&&x<7;x++)for(int w=0;w<2;w++)for(int m=-1;m<2;m+=2){
        if(k+1<np&&x!=pre[k+1]/2)continue;
        W[i]=w;M[i]=m;X[i]=x;set[i]=1;if(x==used)used++;
        memcpy(cp,tape,TW);cp[pos]=w;go(cp,pos+m,x,k+1,nset+1);
        set[i]=0;used=u0;}
      return;}
    tape[pos]=W[i];pos+=M[i];st=X[i];k++;
    if(pos<1||pos>TW-2){partial++;return;}
  }
}
int main(int c,char**v){for(char*p=v[1];*p;p++){if(*p==' ')continue;pre[np++]=(*p>='a')?*p-'a'+10:*p-'0';}
  budget=atol(v[2]);doprint=c>3;unsigned char tape[TW];memset(tape,0,TW);
  go(tape,TW/2,0,0,0);
  fprintf(stderr,"%s | full tables %ld | halted with a wire open %ld | still open after budget %ld\n",v[1],full,halted,partial);}
