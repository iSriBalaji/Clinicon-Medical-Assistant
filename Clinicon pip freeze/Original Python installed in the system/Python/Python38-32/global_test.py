global a

def fun():
    global b
    b=40
    a=10

a=2
b=10
print(a,b)


fun()
print(a,b)
