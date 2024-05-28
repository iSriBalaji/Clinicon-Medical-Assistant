a=10
while(a>5):
    print(a)
    if(a==7):break
    a-=1
else:
    print("It exceeds 5")
print()
for i in range(2,14,2):
    if(i==10): break
    print(i)
else:
    print("Iteration ends")
print()
for i,n in enumerate(list(range(2,14,2))):
    print("i is {} and n is {}".format(i,n))
print()

