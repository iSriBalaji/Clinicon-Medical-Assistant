st = input()
le=len(st)
no = int(input())
ma=0
s=0
for i,n in enumerate(st):
    print(i,n)
    if(n=='1'):
        s+=1
    if((i+1)%no==0 or (i+1)==le):
        if(s>ma):
            ma=s
        s=0
print(ma)
    
    
