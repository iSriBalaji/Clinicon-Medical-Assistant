a=4
try:
    print(a/0)
except e:
    print(e)
else:
    print("Success")
finally:
    print("Done Exception")
