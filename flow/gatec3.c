/* gatec.c STEPS : the gate and the pieces of a machine.  Reads tables (first word of each line), runs each from a blank tape, prints
     table  K  exits  haltdist  p01  p001
   K        = length of the counting loop the halt hangs off: a loop of 2 or 3 digits (like 91 or 159) that repeats at least
              3 times in a row somewhere, and from whose states the halt can be reached within 3 steps.  0 = no such loop.
   exits    = how many different ways the run has left that loop so far (the safe sides of the gate)
   haltdist = steps from the loop to the halt (1 to 3)
   p01, p001 = the longest row of pieces 01 01 01 ... and 001 001 001 ... (or 011 011 ...) seen on the tape */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define W 400000
static char tape[W];static unsigned char*tr_;
int main(int ac,char**av){long NS=atol(av[1]);char line[4096];tr_=malloc(NS+8);
  while(fgets(line,4096,stdin)){char t[64];if(sscanf(line,"%60s",t)!=1||strlen(t)<48)continue;int tr[7][2],nx[14],hd=-1;
    for(int s=0;s<7;s++)for(int b=0;b<2;b++){char*e=t+s*7+b*3;if(e[2]=='Z'){tr[s][b]=-1;nx[2*s+b]=-2;hd=2*s+b;}else if(e[2]=='-'){tr[s][b]=-1;nx[2*s+b]=-1;}else{tr[s][b]=(e[0]-'0')|((e[1]=='R')<<1)|((e[2]-'A')<<2);nx[2*s+b]=e[2]-'A';}}
    memset(tape,0,W);long p=W/2,lo=p,hi=p,n=0;int s=0;int p2=0,p3=0,p4=0;static long pc[14][14];memset(pc,0,sizeof(pc));int pv=-1;
    for(;n<NS;n++){int b=tape[p],d=2*s+b;tr_[n]=d;if(pv>=0)pc[pv][d]++;pv=d;int e=tr[s][b];if(e<0){n++;break;}tape[p]=e&1;p+=(e&2)?1:-1;s=e>>2;if(p<lo)lo=p;if(p>hi)hi=p;if(p<5||p>W-5)break;
      if(n%20000==19999){ /* look for rows of pieces */
        for(long i=lo;i<hi;){long j=i;while(j+1<=hi&&tape[j]!=tape[j+1])j++;int r=(j-i+1)/2;if(r>p2)p2=r;i=j+1;}
        for(long i=lo;i+3<=hi;i++){if(tape[i]+tape[i+1]+tape[i+2]==0||tape[i]+tape[i+1]+tape[i+2]==3)continue;long j=i;while(j+3<=hi&&tape[j]==tape[j+3])j++;int r=(j-i)/3+1;if(r>p3)p3=r;if(j>i)i=j;}
        for(long i=lo;i+4<=hi;i++){int q=tape[i]+tape[i+1]+tape[i+2]+tape[i+3];if(q==0||q==4||(tape[i]==tape[i+2]&&tape[i+1]==tape[i+3]))continue;long j=i;while(j+4<=hi&&tape[j]==tape[j+4])j++;int r=(j-i)/4+1;if(r>p4)p4=r;if(j>i)i=j;}}}
    /* counting loops: cycles of length 2 or 3 repeated >=3 times */
    int bestK=0,bestEx=0,bestD=9;long bestc=0;int bc[3]={0,0,0};
    for(int K=2;K<=3;K++){static long cnt[14][14][14];memset(cnt,0,sizeof(cnt));
      for(long i=0;i+3*K<=n;i++){int ok=1;for(int j=0;j<2*K&&ok;j++)if(tr_[i+j]!=tr_[i+j+K])ok=0;if(!ok)continue;
        if(K==2){if(tr_[i]==tr_[i+1])continue;cnt[tr_[i]][tr_[i+1]][0]++;}else{if(tr_[i]==tr_[i+1]&&tr_[i+1]==tr_[i+2])continue;cnt[tr_[i]][tr_[i+1]][tr_[i+2]]++;}}
      for(int a=0;a<14;a++)for(int b=0;b<14;b++)for(int c=0;c<(K==2?1:14);c++){long cc=cnt[a][b][c];if(cc<1)continue;int cyc[3]={a,b,c};
        /* can the halt be reached within 3 steps from the other symbol of a loop state? */
        int dist=9;for(int j=0;j<K;j++){int cur[16],nc=1;cur[0]=cyc[j]^1;
          for(int dd=1;dd<=3&&nc>0;dd++){int nf[16],m=0;for(int q=0;q<nc;q++){int y=cur[q];if(y==hd){if(dd<dist)dist=dd;}else if(nx[y]>=0&&m<14){nf[m++]=2*nx[y];nf[m++]=2*nx[y]+1;}}
            memcpy(cur,nf,sizeof(int)*m);nc=m;}}
        if(dist==9)continue;
        /* exits used: digits that follow a loop digit and are not the next loop digit */
        int ex[14]={0};for(long i=0;i+1<n;i++){for(int j=0;j<K;j++)if(tr_[i]==cyc[j]&&tr_[i+1]!=cyc[(j+1)%K]){ex[tr_[i+1]]=1;}}
        int ne=0;for(int q=0;q<14;q++)ne+=ex[q];
        if(dist<bestD||(dist==bestD&&cc>bestc)){bestc=cc;bestK=K;bestEx=ne;bestD=dist;bc[0]=cyc[0];bc[1]=cyc[1];bc[2]=cyc[2];}}}
    long visits=0,maxr=0,firstr=0,lastr=0;
    if(bestK){int K=bestK;for(long i=0;i+K<=n;){int ok=1;for(int j=0;j<K;j++)if(tr_[i+j]!=bc[j])ok=0;if(!ok){i++;continue;}
        long r=0,j=i;while(j+K<=n){int o=1;for(int q=0;q<K;q++)if(tr_[j+q]!=bc[q])o=0;if(!o)break;r++;j+=K;}
        if(r>=2){visits++;if(r>maxr)maxr=r;if(!firstr)firstr=r;lastr=r;}i=j>i?j:i+1;}}
    /* the two most used loops (a digit repeating, or two alternating); their exit wires; does the halt hang on one? */
    long l1=0,l2=0;int e1[2]={-1,-1},e2[2]={-1,-1};
    for(int a=0;a<14;a++){long c=pc[a][a];int x0=a^1,x1=-1;if(c>l1){l2=l1;e2[0]=e1[0];e2[1]=e1[1];l1=c;e1[0]=x0;e1[1]=x1;}else if(c>l2){l2=c;e2[0]=x0;e2[1]=x1;}
      for(int b=a+1;b<14;b++){long c2=pc[a][b];if(!c2||!(pc[b][a]*10>c2*8&&c2*10>pc[b][a]*8))continue;c2+=pc[b][a];int y0=a^1,y1=b^1;
        if(c2>l1){l2=l1;e2[0]=e1[0];e2[1]=e1[1];l1=c2;e1[0]=y0;e1[1]=y1;}else if(c2>l2){l2=c2;e2[0]=y0;e2[1]=y1;}}}
    int hang=0,jobs=0,xs[4]={e1[0],e1[1],e2[0],e2[1]};
    for(int q=0;q<4;q++){int x=xs[q];if(x<0||hd<0)continue;long used=0;int preds=0;for(int a=0;a<14;a++)if(pc[a][x]){used+=pc[a][x];preds++;}
      if(!used||nx[x]<0)continue;int S1=nx[x],d=9;if(hd/2==S1)d=1;else for(int y=2*S1;y<=2*S1+1;y++)if(nx[y]>=0&&hd/2==nx[y])d=2;
      if(d<=2){hang=1;if(preds>=2)jobs=1;}}
    printf("%s %d %d %d %d %d %ld %ld %d %d %d\n",t,bestK,bestEx,bestK?bestD:0,p2,p3,visits,maxr,hang,jobs,p4);}
  return 0;}
