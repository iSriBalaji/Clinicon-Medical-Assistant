def fact(n):
    if(n==1):
        return n
    else:
        return n*fact(n-1)


no=int(input())
n=no/2
asc = fact(2*n)
desc = fact(n+1)*fact(n)
ans = asc/desc
print(int(ans))
