st=[3,8]
fi=[4,9]
n=10
ls=[]
for i in range(1,n+1):
    ls.append(i)
for ind in range(0,len(st)):
    for kl in range(st[ind],fi[ind]+1):
        if kl in ls:
            ls.remove(kl)
ma=0
lee=len(ls)
cnt=0
for inn,vi in enumerate(ls):
    if(inn==0 or inn==(lee-1)):
        continue
    if(vi==ls[inn-1]+1):
        cnt+=1
    else:
        cnt=0
        if(cnt>ma):
            ma=cnt
print(ma)
        
    

