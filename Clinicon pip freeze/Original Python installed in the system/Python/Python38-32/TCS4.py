#!/bin/python3

import math
import os
import random
import re
import sys



class Employee:
    dic={}
    def __init__(self,n,i,a,g):
        self.dic['name']=n
        self.dic['id']=i
        self.dic['age']=a
        self.dic['gen']=g

class Organisation:
    elist=[]
    def __init__(self,na,k):
        self.nam=na
        self.elist=[]
    
    def addEmployee(self,n,i,a,g):
        e=Employee(n,i,a,g)
        self.elist.append(e)

    def getEmployeeCount(self):
        for i in self.elist:
            print(i.dic['name'])
        return len(self.elist)

    def findEmployeeAge(self,i):
        for e in range(0,len(self.elist)):
            if (self.elist[e].dic['id']==i):return self.elist[e].dic['age']
        else:
            return -1

    def countEmployees(self,a):
        cnt=0
        for e in range(0,len(self.elist)):
            if(self.elist[e].dic['age']>a):cnt+=1
        return cnt
if __name__ == '__main__':
    employees=[]
    o = Organisation('XYZ',employees)
    n=int(input())
    for i in range(n):
        name=input()
        id=int(input())
        age=int(input())
        gender=input()
        o.addEmployee(name,id,age,gender)

    id=int(input())
    age=int(input())
    print(o.getEmployeeCount())
    print(o.findEmployeeAge(id))
    print(o.countEmployees(age))
