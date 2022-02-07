
import re
import sys
import os
import socket
import warnings
import tkinter as tk
from tkinter.ttk import * 
from tkinter import messagebox
import mysql.connector
from PIL import ImageTk
import PIL.Image as pl 
from tkinter import *
from tkinter import ttk
from win32api import GetSystemMetrics
from datetime import date
from datetime import datetime




########################################################################################## ------------  DATABASE 

def create_db():

    mydb=mysql.connector.connect(
    host="localhost",user="root",
    password="lenovog500s")
    cursor=mydb.cursor()
    a="create database if not exists DISPUR"
    cursor.execute(a)
    cursor.close()

def create_table():
    mydb=mysql.connector.connect(
    host="localhost",
    user="root",
    password="lenovog500s",
    database="DISPUR")
    cursor=mydb.cursor()

    stmt = "SHOW TABLES LIKE 'customer'"
    cursor.execute(stmt)
    
    result = cursor.fetchone()
    print(result)
    if result:
        if "customer" in result:
            print("table exists")
    else:
        print("there are no tables")
        a="create table   if not exists Customer(Reg_Id INT PRIMARY KEY AUTO_INCREMENT , Name VARCHAR(20) NOT NULL , Address VARCHAR(80) NOT NULL , Email VARCHAR(30) NOT NULL , Contact_Number VARCHAR(12),password VARCHAR(20) NOT NULL)"
    
        cursor.execute(a)

        b="alter table Customer AUTO_INCREMENT=509610"
        cursor.execute(b)
    
        a ="insert into customer (Name,Address,Email,Contact_Number,password) values ('Admin','bangalore','abc@gmail.com','1111','admin12345')"
        cursor.execute(a)
    cursor.close()
    mydb.commit()
    mydb.close()
    
def insert_table(data):
    mydb=mysql.connector.connect(
    host="localhost",
    user="root",
    password="lenovog500s",
    database="DISPUR")
    cursor=mydb.cursor()
    us=""" INSERT INTO customer (Name,Address,Email,Contact_Number,password) VALUES (%s,%s,%s,%s,%s) """
    d=(data[0],data[1],data[2],data[3],data[4])
    cursor.execute(us,d)
    cursor.close()
    mydb.commit()
    mydb.close()
    
def update_table(n):
    mydb=mysql.connector.connect(
    host="localhost",
    user="root",
    password="lenovog500s",
    database="DISPUR")
    #dat=(n,a,m,c,p,i)
    print(n)
    cursor=mydb.cursor()
    us=""" UPDATE customer SET Name = %s,Address= %s,Email= %s,Contact_Number= %s,password= %s WHERE Reg_Id = %s """
    cursor.execute(us,(n[0],n[1],n[2],n[3],n[4],int(n[5])))
    cursor.close()
    print("updated")
    mydb.commit()
    mydb.close()
    messagebox.showinfo("Update Profile","Updation Successful! Return to My Profile Page")

def retrieve_data(idd,upas):
    mydb=mysql.connector.connect(
    host="localhost",
    user="root",
    password="lenovog500s",
    database="DISPUR")
    cursor=mydb.cursor()
    data=(idd,upas)
    a="select * from customer where Reg_Id=%s and password=%s "
    cursor.execute(a,data)
    result=cursor.fetchall()
    li=[]
    
    for i in result:
        li.append(i)
    cursor.close()
    mydb.commit()
    mydb.close()
    
    return li

def retrieval_data(n):
    mydb=mysql.connector.connect(
    host="localhost",
    user="root",
    password="lenovog500s",
    database="DISPUR")
    cursor=mydb.cursor()
    
    a="select * from customer where Reg_Id=%s "
    cursor.execute(a,(n,))
    result=cursor.fetchall()
       
    return result

def delete_table():
    mydb=mysql.connector.connect(
    host="localhost",
    user="root",
    password="lenovog500s",
    database="DISPUR")
    cursor=mydb.cursor()
    cursor.execute("DROP TABLE customer")
    cursor.close()
    mydb.commit()
    mydb.close()


def delete_data(n):
    mydb=mysql.connector.connect(
    host="localhost",
    user="root",
    password="lenovog500s",
    database="DISPUR")
    cursor=mydb.cursor()
    a="""Delete from customer where Reg_Id = %s"""
    
    cursor.execute(a,(n,))
    cursor.close()
    mydb.commit()
    mydb.close()
    messagebox.showinfo("Deactivate Account","Your account has been deleted!")
    loginFrame()



def print_data():
    mydb=mysql.connector.connect(
    host="localhost",
    user="root",
    password="lenovog500s",
    database="DISPUR")
    cursor=mydb.cursor()
    cursor.execute("select *from customer")
    result=cursor.fetchall()
    print(result)
    cursor.close()
    mydb.commit()
    mydb.close()

  
create_db()
create_table()
print_data()

#####################################################-------------------REGISTER UI 


def registr():
    try:
        frame2.place_forget()
    except:
        pass
    global frame5
    frame5 = LabelFrame(root,bg="#142850")
    frame5.place(x=500,y=147,height=550,width=700)
    space=Label(frame5,text="      ",bg="#142850",fg="#ffffff",font=("Ubuntu",23,"bold"),anchor=W)
    space.grid(row=0,column=0,sticky=W+E)
    la1=Label(frame5,text="Registration Page",bg="#142850",fg="#fddb3a",font=("Ubuntu",21,"bold"),anchor=W)
    la1.grid(row=1,column=1,sticky=W+E,pady=10)
    name_var=StringVar()
    pswrd_var=StringVar()
    address_var=StringVar()
    email_var=StringVar()
    phone_var=StringVar()

    
    def validate():
        name=name_entry.get()
        if re.match("^[A-Z a-z 0-9 _ .]{4,15}$", name) == None:
            messagebox.showinfo("Registration Page","Username must have atleast 8 to 15 characters")
            name_var.set("")
            
        else:
            password=pswrd_entry.get()
            if re.match("^(?=.*[0-9])(?=.*[A-Z])(?=.*[a-z])(?=.*[! @ # $ . _]).{8,15}$",password) == None:
                messagebox.showinfo("Registration Page","Password must have atleast one special character, Upper case and Lowercase letter and lenght should be 8 to 15 characters")
                pswrd_var.set("")
                
                
            else:
                address=address_entry.get()
                email=email_entry.get()
                if re.match("^[A-Z a-z 0-9 _ .]{4,12}[@][a-z]{3,9}[.][a-z]{2,3}$",email) == None:
                    messagebox.showinfo("Registration Page","Invalid email Id")
                    email_var.set("")
                    
                else:
                    mobile=phone_entry.get()
                    if re.match("^[6-9][0-9]{9}$",mobile) == None:
                        messagebox.showinfo("Registration Page","Invalid Mobile Number")
                        phone_var.set("")
                    else:
                        messagebox.showinfo("Registration Page","Registration Successful! return to login page")
                        n,p,a,e,ph=name_entry.get(),pswrd_entry.get(),address_entry.get(),email_entry.get(),phone_entry.get()
                        details=(n,a,e,ph,p)
                        insert_table(details)                        
                        name_var.set("")
                        pswrd_var.set("")
                        address_var.set("")
                        email_var.set("")
                        phone_var.set("")
                        
    
    name_label = Label(frame5, text = 'Username :',bg="#142850",fg="#ffffff",font=("Ubuntu",16,"bold"),anchor=W)
    name_entry = Entry(frame5,textvariable = name_var,borderwidth=1,fg="#222831",bg="#dae1e7",width=20,font=('Ubuntu',16,"normal"))

    pswrd_label = Label(frame5, text = 'Password :',bg="#142850",fg="#ffffff",font=("Ubuntu",16,"bold"),anchor=W)
    pswrd_entry = Entry(frame5,textvariable = pswrd_var,borderwidth=1,fg="#222831",bg="#dae1e7",width=20,font=('Ubuntu',16,"bold"),show="•")

    address_label=Label(frame5, text = 'Address :',bg="#142850",fg="#ffffff",font=("Ubuntu",16,"bold"),anchor=W)
    address_entry=Entry(frame5,textvariable = address_var,borderwidth=1,fg="#222831",bg="#dae1e7",width=20,font=('Ubuntu',16,"normal"))

    email_label=Label(frame5, text = 'Email Id :',bg="#142850",fg="#ffffff",font=("Ubuntu",16,"bold"),anchor=W)
    email_entry=Entry(frame5,textvariable = email_var,borderwidth=1,fg="#222831",bg="#dae1e7",width=20,font=('Ubuntu',16,"normal"))

    phone_label=Label(frame5, text = 'Mobile number :',bg="#142850",fg="#ffffff",font=("Ubuntu",16,"bold"),anchor=W)
    phone_entry=Entry(frame5,textvariable = phone_var,borderwidth=1,fg="#222831",bg="#dae1e7",width=20,font=('Ubuntu',16,"normal"))

    register_btn=Button(frame5,text = 'Register',bg="#00909e",fg="#dae1e7",font=("Ubuntu",16,"bold"),command = validate)

    name_label.grid(row=2,column=1,sticky=W+E,padx=8,pady=8)
    name_entry.grid(row=2,column=2,padx=8,pady=8)

    pswrd_label.grid(row=3,column=1,sticky=W+E,padx=8,pady=8)
    pswrd_entry.grid(row=3,column=2,padx=8,pady=8)

    address_label.grid(row=4,column=1,sticky=W+E,padx=8,pady=8)
    address_entry.grid(row=4,column=2,padx=8,pady=8)

    email_label.grid(row=5,column=1,sticky=W+E,padx=8,pady=8)
    email_entry.grid(row=5,column=2,padx=8,pady=8)

    phone_label.grid(row=6,column=1,sticky=W+E,padx=8,pady=8)
    phone_entry.grid(row=6,column=2,padx=8,pady=8)

    register_btn.grid(row=7,column=1,columnspan=2,padx=8,pady=8)
    
    loginbtn=Button(frame5,text = "Login",bg="#00909e",fg="#dae1e7",font=("Ubuntu",16,"bold"),command = loginFrame)
    loginbtn.grid(row=7,column=2,columnspan=2,padx=8,pady=8)

####################################################################################################-------------------Login UI        

#Getting Screen Height and Width of the device
screen_width = GetSystemMetrics(0) #864
screen_height = GetSystemMetrics(1) #1536

#Icons
icon_path=os.path.join(os.path.dirname(__file__),"pictures/radar.ico")

#Getting Date and Time
today = date.today()
now = datetime.now()
warnings.filterwarnings("ignore")

#Getting IP
hostname = socket.gethostname()    
ip_add = socket.gethostbyname(hostname)

#Update Time in real time
def updateTime():
    now = datetime.now()
    current_time=now.strftime("%H:%M:%S")
    lab5["text"]=str(current_time)+"\n"
    root.after(200,updateTime)

def updateProfile(data):
    #update the DB
    print("profile")
    update_table(data)

def retrieve(n):
    d=" "
    print("retrieval of data")
    name_e1.delete(0,END)    
    pswd_e1.delete(0,END)
    add_e1.delete(0,END)
    mail_e1.delete(0,END)
    contact_e1.delete(0,END)
    details=retrieval_data(n)
    print(details)
    name_e1.insert(0,details[0][1])    
    pswd_e1.insert(0,details[0][-1])
    add_e1.insert(0,details[0][2])
    mail_e1.insert(0,details[0][3])
    contact_e1.insert(0,details[0][4])

def delete(n):
    print("deleting",n)
    delete_data(n)

def login():
    idd=reg_en.get()
    reg_en.delete(0,END)

    u_pas=pas_en.get()
    pas_en.delete(0,END)

    res=retrieve_data(idd,u_pas)
    print("start",res,"Return valus")
    if(len(res) !=0):
        print("1st if",res[0][0])
        if(str(idd)==str(res[0][0]) and u_pas==res[0][5]):
            print("2nd if")
            if(str(res[0][0])=="50965" and res[0][5]=="admin12345"):
                print("3rd if admin")
                frame2.place_forget()
                adminProfile()
            else:  
                frame2.place_forget()
                print("in loop")
                myProfile(res[0])

    else:
        temp["text"]="username or password is incorrect!"


def myProfile(res):
    pass
def loginFrame():
    pass
def adminProfile():
    try:
        frame2.place_forget()
        frame3.place_forget()
    except:
        pass
    global frame7
    frame7 = LabelFrame(root,bg="#142850")
    frame7.place(x=500,y=147,height=550,width=700)
    space=Label(frame7,text="      ",bg="#142850",fg="#ffffff",font=("Ubuntu",23,"bold"),anchor=W)
    space.grid(row=0,column=0,sticky=W+E)
    lab1=Label(frame7,text="Admin Portal",bg="#142850",fg="#fddb3a",font=("Ubuntu",21,"bold"),anchor=W)
    lab1.grid(row=1,column=1,sticky=W+E,pady=10)

    uid=Label(frame7,text="ID: ",bg="#142850",fg="#2ec1ac",font=("Ubuntu",16,"bold"),anchor=W)
    uid.grid(row=2,column=1,sticky=W+E,padx=8,pady=8)
    name=Label(frame7,text="Name: ",bg="#142850",fg="#2ec1ac",font=("Ubuntu",16,"bold"),anchor=W)
    name.grid(row=6,column=1,sticky=W+E,padx=8,pady=8)
    pswd=Label(frame7,text="Password: ",bg="#142850",fg="#2ec1ac",font=("Ubuntu",16,"bold"),anchor=W)
    pswd.grid(row=7,column=1,sticky=W+E,padx=8,pady=8)
    address=Label(frame7,text="Address: ",bg="#142850",fg="#2ec1ac",font=("Ubuntu",16,"bold"),anchor=W)
    address.grid(row=8,column=1,sticky=W+E,padx=8,pady=8)
    email=Label(frame7,text="Email ID: ",bg="#142850",fg="#2ec1ac",font=("Ubuntu",16,"bold"),anchor=W)
    email.grid(row=9,column=1,sticky=W+E,padx=8,pady=8)
    contact=Label(frame7,text="Contact: ",bg="#142850",fg="#2ec1ac",font=("Ubuntu",16,"bold"),anchor=W)
    contact.grid(row=10,column=1,sticky=W+E,padx=8,pady=8)
    
    global uid_e1
    uid_e1=Entry(frame7,text="id",borderwidth=1,fg="#222831",bg="#dae1e7",width=20,font=('Ubuntu',16,"bold"))
    uid_e1.insert(0,"")
    uid_e1.grid(row=2,column=2,padx=8,pady=8)
    det_button = Button(frame7,text="Get Details",width=18,bg="#00909e",fg="#dae1e7",font=("Ubuntu",16,"bold"),command=lambda:retrieve(int(uid_e1.get())))
    det_button.grid(row=3,column=2,columnspan=2,padx=8,pady=8,sticky=W)

    
    
    global name_e1
    name_e1= Entry(frame7,text="name",borderwidth=1,fg="#222831",bg="#dae1e7",width=20,font=('Ubuntu',16,"bold"))
    #name_e1.insert(0,details[1])
    name_e1.grid(row=6,column=2,padx=8,pady=8)
    global pswd_e1
    pswd_e1= Entry(frame7,text="pswd",borderwidth=1,fg="#222831",bg="#dae1e7",width=20,font=('Ubuntu',16,"bold"),show="•")
    #pswd_e1.insert(0,details[-1])
    pswd_e1.grid(row=7,column=2,padx=8,pady=8)
    global add_e1
    add_e1 = Entry(frame7,text="address",borderwidth=1,fg="#222831",bg="#dae1e7",width=20,font=('Ubuntu',16,"bold"))
    #add_e1.insert(0,details[2])
    add_e1.grid(row=8,column=2,padx=8,pady=8)
    global mail_e1
    mail_e1 = Entry(frame7,text="mail",borderwidth=1,fg="#222831",bg="#dae1e7",width=20,font=('Ubuntu',16,"bold"))
    #mail_e1.insert(0,details[3])
    mail_e1.grid(row=9,column=2,padx=8,pady=8)
    global contact_e1
    contact_e1= Entry(frame7,text="contact",borderwidth=1,fg="#222831",bg="#dae1e7",width=20,font=('Ubuntu',16,"bold"))
    #contact_e1.insert(0,details[4])
    contact_e1.grid(row=10,column=2,padx=8,pady=8)

    update = Button(frame7,text="Update",bg="#00909e",fg="#dae1e7",font=("Ubuntu",16,"bold"),command=lambda:updateProfile((str(name_e1.get()),str(add_e1.get()),str(mail_e1.get()),str(contact_e1.get()),str(pswd_e1.get()),str(uid_e1.get()))))
    update.grid(row=11,column=2,columnspan=2,padx=8,pady=8,sticky=W)
    
    home = Button(frame7,text="Home",bg="#00909e",fg="#dae1e7",font=("Ubuntu",16,"bold"),command=loginFrame)
    home.grid(row=1,column=3,columnspan=2,padx=8,pady=8)
    g=str(uid_e1.get())
    print(g)
    delete_p= Button(frame7,text="Delete",bg="#00909e",fg="#dae1e7",font=("Ubuntu",16,"bold"),command=lambda:delete(int(uid_e1.get())))
    delete_p.grid(row=11,column=2,columnspan=2,padx=8,pady=8)
   
    
    
###########################################
def editProfile(details):
    try:
        frame2.place_forget()
        frame3.place_forget()
    except:
        pass
    global frame4
    frame4 = LabelFrame(root,bg="#142850")
    frame4.place(x=500,y=147,height=550,width=700)
    space=Label(frame4,text="      ",bg="#142850",fg="#ffffff",font=("Ubuntu",23,"bold"),anchor=W)
    space.grid(row=0,column=0,sticky=W+E)
    lab1=Label(frame4,text="EDIT PROFILE",bg="#142850",fg="#fddb3a",font=("Ubuntu",21,"bold"),anchor=W)
    lab1.grid(row=1,column=1,sticky=W+E,pady=10)

    uid=Label(frame4,text="ID: ",bg="#142850",fg="#2ec1ac",font=("Ubuntu",16,"bold"),anchor=W)
    uid.grid(row=2,column=1,sticky=W+E,padx=8,pady=8)
    name=Label(frame4,text="Name: ",bg="#142850",fg="#2ec1ac",font=("Ubuntu",16,"bold"),anchor=W)
    name.grid(row=3,column=1,sticky=W+E,padx=8,pady=8)
    pswd=Label(frame4,text="Password: ",bg="#142850",fg="#2ec1ac",font=("Ubuntu",16,"bold"),anchor=W)
    pswd.grid(row=4,column=1,sticky=W+E,padx=8,pady=8)
    address=Label(frame4,text="Address: ",bg="#142850",fg="#2ec1ac",font=("Ubuntu",16,"bold"),anchor=W)
    address.grid(row=5,column=1,sticky=W+E,padx=8,pady=8)
    email=Label(frame4,text="Email ID: ",bg="#142850",fg="#2ec1ac",font=("Ubuntu",16,"bold"),anchor=W)
    email.grid(row=6,column=1,sticky=W+E,padx=8,pady=8)
    contact=Label(frame4,text="Contact: ",bg="#142850",fg="#2ec1ac",font=("Ubuntu",16,"bold"),anchor=W)
    contact.grid(row=7,column=1,sticky=W+E,padx=8,pady=8)
    plan=Label(frame4,text="Blood Group: ",bg="#142850",fg="#2ec1ac",font=("Ubuntu",16,"bold"),anchor=W)
    plan.grid(row=8,column=1,sticky=W+E,padx=8,pady=8)

    uid_e = Label(frame4,text=details[0],bg="#142850",fg="#ffffff",font=("Ubuntu",16,"bold"),anchor=W)
    uid_e.grid(row=2,column=2,padx=8,pady=8)
    name_e = Entry(frame4,text="name",borderwidth=1,fg="#222831",bg="#dae1e7",width=20,font=('Ubuntu',16))
    name_e.delete(0,END)
    name_e.insert(0,details[1])
    name_e.grid(row=3,column=2,padx=8,pady=8)
    pswd_e = Entry(frame4,text="pswd",borderwidth=1,fg="#222831",bg="#dae1e7",width=20,font=('Ubuntu',16,"bold"),show="•")
    pswd_e.delete(0,END)
    pswd_e.insert(0,details[-1])
    pswd_e.grid(row=4,column=2,padx=8,pady=8)
    add_e = Entry(frame4,text="address",borderwidth=1,fg="#222831",bg="#dae1e7",width=20,font=('Ubuntu',16))
    add_e.delete(0,END)
    add_e.insert(0,details[2])
    add_e.grid(row=5,column=2,padx=8,pady=8)
    mail_e = Entry(frame4,text="mail",borderwidth=1,fg="#222831",bg="#dae1e7",width=20,font=('Ubuntu',16))
    mail_e.delete(0,END)
    mail_e.insert(0,details[3])
    mail_e.grid(row=6,column=2,padx=8,pady=8)
    contact_e = Entry(frame4,text="contact",borderwidth=1,fg="#222831",bg="#dae1e7",width=20,font=('Ubuntu',16))
    contact_e.delete(0,END)
    contact_e.insert(0,details[4])
    contact_e.grid(row=7,column=2,padx=8,pady=8)
    plan_select= ttk.Combobox(frame4, width = 18,foreground="#222831",background="#dae1e7",font=('Ubuntu',16))
    plan_select['values'] = ("O+","O-","A+","A-","B+","B-","AB+","AB-")
    plan_select.grid(row=8,column=2,padx=8,pady=8)
    plan_select.current(2)

    n,a,m,c,p,i=str(name_e.get()),str(add_e.get()),str(mail_e.get()),str(contact_e.get()),str(pswd_e.get()),str(details[0])
    #update = Button(frame4,text="Update",width=4,height=3,command=updateProfile(n,a,m,c,p,i))
    update = Button(frame4,text="Update",bg="#00909e",fg="#dae1e7",font=("Ubuntu",16,"bold"),command=lambda:updateProfile((str(name_e.get()),str(add_e.get()),str(mail_e.get()),str(contact_e.get()),str(pswd_e.get()),str(details[0]))))
    update.grid(row=10,column=2,columnspan=2,padx=8,pady=8,sticky=W)
    
    home = Button(frame4,text="Home",bg="#00909e",fg="#dae1e7",font=("Ubuntu",16,"bold"),command=loginFrame)
    home.grid(row=1,column=3,columnspan=2,padx=8,pady=8,sticky=E)

    delete_p= Button(frame4,text="Delete",bg="#00909e",fg="#dae1e7",font=("Ubuntu",16,"bold"),command=lambda:delete_data(int(details[0])))
    delete_p.grid(row=10,column=2,columnspan=2,padx=8,pady=8)
    name_e.insert(0," ")
    contact_e.insert(0," ")
    


def myProfile(res):
    global frame3
    frame3 = LabelFrame(root,bg="#142850")
    frame3.place(x=500,y=147,height=550,width=700)
    space=Label(frame3,text="      ",bg="#142850",fg="#ffffff",font=("Ubuntu",23,"bold"),anchor=W)
    space.grid(row=0,column=0,sticky=W+E)
    la1=Label(frame3,text="MY PROFILE",bg="#142850",fg="#fddb3a",font=("Ubuntu",21,"bold"),anchor=W)
    la1.grid(row=1,column=1,sticky=W+E,pady=10)
    edit_button=Button(frame3,image=edit_pen,height=32,width=32,command=lambda:editProfile(res),bg="#00909e")
    edit_button.grid(row=1,column=2,pady=10,padx=0,sticky=W)

    name=Label(frame3,text="Name: ",bg="#142850",fg="#2ec1ac",font=("Ubuntu",16,"bold"),anchor=W)
    name.grid(row=2,column=1,sticky=W+E,padx=8,pady=8)
    reg_id=Label(frame3,text="Registration ID: ",bg="#142850",fg="#2ec1ac",font=("Ubuntu",16,"bold"),anchor=W)
    reg_id.grid(row=3,column=1,sticky=W+E,padx=8,pady=8)
    address=Label(frame3,text="Address: ",bg="#142850",fg="#2ec1ac",font=("Ubuntu",16,"bold"),anchor=W)
    address.grid(row=4,column=1,sticky=W+E,padx=8,pady=8)
    email=Label(frame3,text="Email ID: ",bg="#142850",fg="#2ec1ac",font=("Ubuntu",16,"bold"),anchor=W)
    email.grid(row=5,column=1,sticky=W+E,padx=8,pady=8)
    contact=Label(frame3,text="Contact: ",bg="#142850",fg="#2ec1ac",font=("Ubuntu",16,"bold"),anchor=W)
    contact.grid(row=6,column=1,sticky=W+E,padx=8,pady=8)
    plan=Label(frame3,text="Broadband Plan: ",bg="#142850",fg="#2ec1ac",font=("Ubuntu",16,"bold"),anchor=W)
    plan.grid(row=7,column=1,sticky=W+E,padx=8,pady=8)

    #retrive data
    ls=res

    name_p=Label(frame3,text=ls[1],bg="#142850",fg="#ffffff",font=("Ubuntu",16,"bold"),anchor=W)
    name_p.grid(row=2,column=2,sticky=W+E,padx=8,pady=8)
    reg_id_p=Label(frame3,text=ls[0],bg="#142850",fg="#ffffff",font=("Ubuntu",16,"bold"),anchor=W)
    reg_id_p.grid(row=3,column=2,sticky=W+E,padx=8,pady=8)
    address_p=Label(frame3,text=ls[2],bg="#142850",fg="#ffffff",font=("Ubuntu",16,"bold"),anchor=W)
    address_p.grid(row=4,column=2,sticky=W+E,padx=8,pady=8)
    email_p=Label(frame3,text=ls[3],bg="#142850",fg="#ffffff",font=("Ubuntu",16,"bold"),anchor=W)
    email_p.grid(row=5,column=2,sticky=W+E,padx=8,pady=8)
    contact_p=Label(frame3,text=ls[4],bg="#142850",fg="#ffffff",font=("Ubuntu",16,"bold"),anchor=W)
    contact_p.grid(row=6,column=2,sticky=W+E,padx=8,pady=8)
    plan_p=Label(frame3,text="Blast Promo",bg="#142850",fg="#ffffff",font=("Ubuntu",16,"bold"),anchor=W)
    plan_p.grid(row=7,column=2,sticky=W+E,padx=8,pady=8)

    bill = Button(frame3,text="Pay Bill",bg="#00909e",fg="#dae1e7",font=("Ubuntu",16,"bold"))
    bill.grid(row=8,column=2,columnspan=2,padx=8,pady=8,sticky=E)
    
    home = Button(frame3,text="Home",bg="#00909e",fg="#dae1e7",font=("Ubuntu",16,"bold"),command=loginFrame)
    home.grid(row=8,column=2,columnspan=2,padx=8,pady=8,sticky=W)



    

def loginFrame():
    global frame2
    frame2 = LabelFrame(root,bg="#142850")
    frame2.place(x=500,y=147,height=550,width=700)
    sp=Label(frame2,text="      ",bg="#142850",fg="#ffffff",font=("Ubuntu",23,"bold"),anchor=W)
    sp.grid(row=0,column=0,sticky=W+E)
    l1=Label(frame2,text="LOGIN",bg="#142850",fg="#fddb3a",font=("Ubuntu",21,"bold"),anchor=W)
    l1.grid(row=1,column=1,sticky=W+E)
    l2=Label(frame2,text="Use your Clinicon or Medilab Account\n",bg="#142850",fg="#ffffff",font=("Ubuntu",12,"bold"),anchor=W)
    l2.grid(row=2,column=1,sticky=W+E)


    reg=Label(frame2,text="MediLab ID: ",bg="#142850",fg="#ffffff",font=("Ubuntu",16,"bold"),anchor=W)
    reg.grid(row=4,column=1,sticky=W+E,padx=8,pady=8)
    pas=Label(frame2,text="Password: ",bg="#142850",fg="#ffffff",font=("Ubuntu",16,"bold"),anchor=W)
    pas.grid(row=5,column=1,sticky=W+E,padx=8,pady=8)

    global reg_en
    global pas_en
    reg_en = Entry(frame2,text="user_id",borderwidth=1,fg="#222831",bg="#dae1e7",width=20,font=('Ubuntu',16,"bold"))
    reg_en.grid(row=4,column=2,padx=8,pady=8)
    pas_en = Entry(frame2,text="user_pass",borderwidth=1,fg="#222831",bg="#dae1e7",width=20,font=('Ubuntu',16,"bold"),show="•")
    pas_en.grid(row=5,column=2,padx=8,pady=8)

    submit = Button(frame2,text="Submit",bg="#00909e",fg="#dae1e7",font=("Ubuntu",16,"bold"),command=login)
    submit.grid(row=6,column=2,columnspan=2,padx=8,pady=8,sticky=W)

    register = Button(frame2,text="Sign Up",bg="#00909e",fg="#dae1e7",font=("Ubuntu",16,"bold"),command=registr)
    register.grid(row=6,column=2,columnspan=2,padx=8,pady=8,sticky=E)
    

    #frame1.place_forget()
    global temp
    temp=Label(frame2,text="",bg="#142850",fg="#e50002",font=("Ubuntu",12,"bold"),anchor=W)
    temp.grid(row=7,column=1,sticky=W+E,columnspan=2)

def welcomeFrame():
    global frame1
    frame1 = Frame(root,bg="#dae1e7",relief=GROOVE)
    frame1.place(x=45,y=107,height=667,width=317)
    lab1=Label(frame1,text="Welcome!",bg="#dae1e7",fg="#142850",font=("Ubuntu",21,"bold"),anchor=W)
    lab1.grid(row=0,column=0,sticky=W+E)
    lab2=Label(frame1,text="Date",bg="#dae1e7",fg="#142850",font=("Ubuntu",14,'underline',"bold"),anchor=W)
    lab2.grid(row=2,column=0,sticky=W+E)
    lab3=Label(frame1,text=today.strftime("%B %d, %Y")+"\n",bg="#dae1e7",fg="#00909e",font=("Ubuntu",16,"bold"),anchor=W)
    lab3.grid(row=3,column=0,sticky=W+E)
    lab4=Label(frame1,text="Local Time",bg="#dae1e7",fg="#142850",font=("Ubuntu",14,'underline',"bold"),anchor=W)
    lab4.grid(row=4,column=0,sticky=W+E)
    global lab5
    lab5=Label(frame1,text=now.strftime("%H:%M:%S")+"\n",bg="#dae1e7",fg="#00909e",font=("Ubuntu",16,"bold"),anchor=W)
    lab5.grid(row=5,column=0,sticky=W+E)
    lab6=Label(frame1,text="Location",bg="#dae1e7",fg="#142850",font=("Ubuntu",14,'underline',"bold"),anchor=W)
    lab6.grid(row=6,column=0,sticky=W+E)
    lab7=Label(frame1,text="India\n",bg="#dae1e7",fg="#00909e",font=("Ubuntu",16,"bold"),anchor=W)
    lab7.grid(row=7,column=0,sticky=W+E)
    lab8=Label(frame1,text="Your IP",bg="#dae1e7",fg="#142850",font=("Ubuntu",14,'underline',"bold"),anchor=W)
    lab8.grid(row=8,column=0,sticky=W+E)
    lab9=Label(frame1,text=ip_add,bg="#dae1e7",fg="#00909e",font=("Ubuntu",16,"bold"),anchor=W)
    lab9.grid(row=9,column=0,sticky=W+E)

root=Tk()
root.title("MEDILAB - Patient Management")
root.iconbitmap(icon_path)
root.state('zoomed')
root.configure(bg="#dae1e7")
#root.attributes('-fullscreen', True)
root.geometry(str(screen_width)+"x"+str(screen_height))

constant_label=Label(root,text="MEDILAB",bg="#dae1e7",fg="#142850",font=("Ubuntu",34,"bold"))
constant_label.place(x=27,y=27)

edit_pen=ImageTk.PhotoImage(pl.open(os.path.join(os.path.dirname(__file__),"pictures/pencil.png")))

welcomeFrame()
updateTime()
loginFrame()
root.mainloop()

#details=('j','asdas','dd@gmail.com',00000,'12345')

print_data()
#delete_table()
