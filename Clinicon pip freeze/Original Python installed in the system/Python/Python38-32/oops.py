#Code - Baju
#Copyright by Baju Kutty
class Sri:
    sub="Subject of the student"
    def __init__(self,sno,name,rollno):
        self.sno=sno
        self.name=name
        self.rollno=rollno

    def gsno(self):
        print("Sno %d"%(self.sno))

    def gname(self):
        print("Name %s"%(self.name))

    def grollno(self):
        print("Rollno %d"%(self.rollno))
        
    def ssno(self,v):
        self.sno=v

    def sname(self,v):
        self.name=v

    def srollno(self,v):
        self.rollno=v

ob1=Sri(1,'Sri',83)
ob2=Sri(2,'Baju',80)
ob3=Sri(3,'Abhi',1)
print("--- Printing the values---")
for i in (ob1,ob2,ob3):
    i.grollno()
    i.gsno()
    i.gname()
    print()
ob1.sub="Maths"
print(ob1.sub) #instance variable
print(Sri.sub) #class variable
#setting values
ob1.ssno(4)
ob2.ssno(5)
ob3.sname("Aki")
ob3.srollno(3)
print("--- Again Printing the values---")
for i in (ob1,ob2,ob3):
    i.grollno()
    i.gsno()
    i.gname()
    print(i.sub)
    print()

print("doc",Sri.__doc__)
print()
print("name",Sri.__name__)
print()
print("module",Sri.__module__)
print()
print("bases",Sri.__bases__)
print()
print("dict",Sri.__dict__)
print()
