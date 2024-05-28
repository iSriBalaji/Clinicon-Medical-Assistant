class Student:
    def __init__(self,rollno,firstname,lastname):
        self.rollno=rollno
        self.firstname=firstname
        self.lastname=lastname
    def __str__(self):
        s_rollno=str(self.rollno)
        return s_rollno+":"+self.firstname+""+self.lastname
s=Student(34,"bas","kar")
print(s)
