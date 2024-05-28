import random
import os
class PassGenerator:
    gen_list=[]
    pas=""
    num=list(range(48,57))
    al=list(range(65,91))+list(range(97,122))
    sym=list(range(32,48))+list(range(58,65))+list(range(91,96))+list(range(123,127))
    def __init__(self,total,letter,number):
        self.appLet(letter)
        self.appNum(number)
        self.appSym(total-(letter+number))
        random.shuffle(self.gen_list)
    def appLet(self,l):
        while(l!=0):
            self.gen_list.append(chr(random.choice(PassGenerator.al)))
            l-=1
    def appNum(self,n):
        while(n!=0):
            self.gen_list.append(chr(random.choice(PassGenerator.num)))
            n-=1
    def appSym(self,s):
        while(s!=0):
            self.gen_list.append(chr(random.choice(PassGenerator.sym)))
            s-=1
    def getPass(self):
        for i in self.gen_list:self.pas+=i
        return self.pas
    
print("\n--------------------------------------------------".center(20,'-'))
print("\n************Hello %s************"%(os.getlogin()))
print()
input("Press any key to Continue...")
print("\n------------------------------".center(20,'-'))
print("WELCOME TO PASSWORD GENERATOR".center(20,' '))
print("------------------------------".center(20,'-'))
while(1):
    try:
        t=int(input("Enter the length of Password to be generated: "))
        while(t<6):
            print("Password must be atleast 6 characters...")
            t=int(input("Enter the length of Password to be generated: "))
    except ValueError as e:
        print("Kindly enter a numeric value!!")
        continue
    l=int(input("Enter the number of letters that has to be present in it: "))
    n=int(input("Enter the number of numeric that has to be present in it: "))
    while(l+n>t):
        print("Limit Exceeded...")
        l=int(input("Enter the number of letters that has to be present in it: "))
        n=int(input("Enter the number of numeric that has to be present in it: "))
    ob=PassGenerator(t,l,n)
    print("\nGenerated Password: %s"%(ob.getPass()))
    print("------------------------------".center(20,'-'))
    if(input("Do you want to create another Password(Y/N):\n") not in ['Y','y']):
        break
    ob.gen_list.clear()
    ob.pas=""
print("%s!! Thanks for visiting Baju's Password Generator\n"%(os.getlogin()))
