from PIL import ImageTk
import PIL.Image as pl             #Image is a module not a class so we've to call like this
from tkinter import *
root=Tk()
root.title("Gview")
root.configure(background="#bfe6ff")
root.resizable(0,0)                     #disables the maximize button

ph=PhotoImage(file=r"C:\Users\Sri Balaji\Desktop\Sri Tut\Baju_Tkinter\Image Viewer\icon.png")
root.iconphoto(False,ph)

def fun(n):
    global forward                   #global variable should be declared inside the function to make it work here
    global back                      #if we were declaring outside it's not working
    global img_label
    
    if(n==9):
        forward=Button(root,text=">>",state=DISABLED,activebackground="#26abff",activeforeground="#ffffff",fg="#ffffff",bg="#26abff",font=('Ubuntu',10,"bold"))
    else:
        forward=Button(root,text=">>",command=lambda:fun(n+1),activebackground="#26abff",activeforeground="#ffffff",fg="#ffffff",bg="#26abff",font=('Ubuntu',10,"bold"))
        forward.grid(row=2,column=2)
    
    img_label.grid_forget()           #it will forget or destroy the current grid
    img_label=Label(root,image=ls[n],padx=5,pady=5)
    img_label.grid(row=1,column=0,columnspan=3)

    img_no=Label(root,text=str(n+1)+"/4",fg="#ffffff",bg="#009dff",font=('Ubuntu',10,"bold"),padx=5,pady=4)
    img_no.grid(row=2,column=1,padx=5,pady=10)
    
    back=Button(root,text="<<",command=lambda:bac(n-1),activebackground="#26abff",activeforeground="#ffffff",fg="#ffffff",bg="#26abff",font=('Ubuntu',10,"bold"))
    back.grid(row=2,column=0)


def bac(n):
    global forward  
    global back                      
    global img_label
    
    if(n==0):
        back=Button(root,text="<<",state=DISABLED,activebackground="#26abff",activeforeground="#ffffff",fg="#ffffff",bg="#26abff",font=('Ubuntu',10,"bold"))
    else:
        back=Button(root,text="<<",command=lambda:bac(n-1),activebackground="#26abff",activeforeground="#ffffff",fg="#ffffff",bg="#26abff",font=('Ubuntu',10,"bold"))
    back.grid(row=2,column=0)

    img_label.grid_forget()         
    img_label=Label(root,image=ls[n],padx=5,pady=5)
    img_label.grid(row=1,column=0,columnspan=3)

    img_no=Label(root,text=str(n+1)+"/4",fg="#ffffff",bg="#009dff",font=('Ubuntu',10,"bold"),padx=5,pady=4)
    img_no.grid(row=2,column=1,padx=5,pady=10)
    
    forward=Button(root,text=">>",command=lambda:fun(n+1),activebackground="#26abff",activeforeground="#ffffff",fg="#ffffff",bg="#26abff",font=('Ubuntu',10,"bold"))
    forward.grid(row=2,column=2)
    
    





i1=ImageTk.PhotoImage(pl.open(r"C:\Users\Sri Balaji\Desktop\Sri Tut\Baju_Tkinter\Image Viewer\img1.png"))
i2=ImageTk.PhotoImage(pl.open(r"C:\Users\Sri Balaji\Desktop\Sri Tut\Baju_Tkinter\Image Viewer\img2.png"))
i3=ImageTk.PhotoImage(pl.open(r"C:\Users\Sri Balaji\Desktop\Sri Tut\Baju_Tkinter\Image Viewer\img3.png"))
i4=ImageTk.PhotoImage(pl.open(r"C:\Users\Sri Balaji\Desktop\Sri Tut\Baju_Tkinter\Image Viewer\img4.png"))

ls=[i1,i2,i3,i4]

img_label=Label(root,image=ls[0],padx=5,pady=5)
img_label.grid(row=1,column=0,columnspan=3)

forward=Button(root,text=">>",command=lambda:fun(1),activebackground="#26abff",activeforeground="#ffffff",fg="#ffffff",bg="#26abff",font=('Ubuntu',10,"bold"))
back=Button(root,text="<<",state=DISABLED,activebackground="#26abff",activeforeground="#ffffff",fg="#ffffff",bg="#26abff",font=('Ubuntu',10,"bold"))
exbutton=Button(root,text="Exit",command=root.quit,activebackground="#eb5a46",activeforeground="#ffffff",fg="#ffffff",bg="#eb5a46",font=('Ubuntu',10,"bold"))

img_no=Label(root,text="1/4",fg="#ffffff",bg="#009dff",font=('Ubuntu',10,"bold"),padx=5,pady=4)
img_no.grid(row=2,column=1,padx=5,pady=10)

forward.grid(row=2,column=2)
back.grid(row=2,column=0)
exbutton.grid(row=3,column=1,padx=5,pady=7)

#Status Bar
#Sunken shows like it as a status bar and anchor allign the text to East(right)
st=Label(root,text="Medilab Analytics",relief=SUNKEN,anchor=E,fg="#ffffff",bg="#009dff",font=('Ubuntu',8,"bold italic"),padx=5,pady=4)  
st.grid(row=4,column=0,columnspan=3,sticky=E+W)                                                                          #sticky grid the label by expanding it to east(right) and west(left)




root.mainloop()
