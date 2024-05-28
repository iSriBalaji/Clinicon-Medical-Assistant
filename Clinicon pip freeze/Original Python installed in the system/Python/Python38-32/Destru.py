class Con:
    gl=80
    def __init__(self):
        self.gl=5
        print("Const")
    def __del__(self):
        nidhi=self.__class__.__name__
        print("Deleted")

a=Con()
print(a.gl)
del Con.gl
b=Con()
try:
    print(Con.gl)
except Exception as e:
    print(e)
else:
    print("Didn't Deleted")
