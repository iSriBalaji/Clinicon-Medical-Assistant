def myfunc(n):
  return lambda a : a+n

mydoubler = myfunc(2) #a=a+2

print(mydoubler(11))
