from tkinter import *
from PIL import Image,ImageTk
root=Tk()
root.title("Baju Calci")
root.configure(background='grey')
#root.iconbitmap("ree.ico")
#root.geometry("300x300")
myE=Entry(root,fg="#00ff00",bg="black",borderwidth=2)
myE.grid(row=0,column=0,columnspan=3,padx=10,pady=10)
#creating image
myii=ImageTk.PhotoImage(Image.open("ic.png"))
ml=Label(image=myii)
#define fn
def clic(a):
    myE.insert(0,a)
def evv():
    va=myE.get()
    myE.delete(0,END)
    ans=eval(va)
    print(va)
    print(ans)
    myE.insert(0,ans)
def dee():
    myE.delete(0,END)
#creating Buttons
b1=Button(root,text="1",fg="white",bg="black",command=lambda:clic(1))
b1.grid(row=1,column=0,padx=3,pady=3)
b2=Button(root,text="2",fg="white",bg="black",command=lambda:clic(2))
b2.grid(row=1,column=1,padx=3,pady=3)
b3=Button(root,text="3",fg="white",bg="black",command=lambda:clic(3))
b3.grid(row=1,column=2,padx=3,pady=3)
b4=Button(root,text="4",fg="white",bg="black",command=lambda:clic(4))
b4.grid(row=2,column=0,padx=3,pady=3)
b5=Button(root,text="5",fg="white",bg="black",command=lambda:clic(5))
b5.grid(row=2,column=1,padx=3,pady=3)
b6=Button(root,text="6",fg="white",bg="black",command=lambda:clic(6))
b6.grid(row=2,column=2,padx=3,pady=3)
b7=Button(root,text="7",fg="white",bg="black",command=lambda:clic(7))
b7.grid(row=3,column=0,padx=3,pady=3)
b8=Button(root,text="8",fg="white",bg="black",command=lambda:clic(8))
b8.grid(row=3,column=1,padx=3,pady=3)
b9=Button(root,text="9",fg="white",bg="black",command=lambda:clic(9))
b9.grid(row=3,column=2,padx=3,pady=3)
b0=Button(root,text="0",fg="white",bg="black",command=lambda:clic(0))
b0.grid(row=4,column=0,padx=3,pady=3)

ad=Button(root,text="+",fg="white",bg="black",command=lambda:clic('+'))
ad.grid(row=4,column=1,padx=3,pady=3)

su=Button(root,text="-",fg="white",bg="black",command=lambda:clic('-'))
su.grid(row=5,column=0,padx=3,pady=3)
mu=Button(root,text="*",fg="white",bg="black",command=lambda:clic('*'))
mu.grid(row=5,column=1,padx=3,pady=3)
di=Button(root,text="/",fg="white",bg="black",command=lambda:clic('/'))
di.grid(row=5,column=2,padx=3,pady=3)

eqq=Button(root,text="=",fg="white",bg="black",command=evv)
eqq.grid(row=4,column=2,padx=3,pady=3)

cl=Button(root,text="Clear",fg="white",bg="black",command=dee)
cl.grid(row=6,column=0,columnspan=2,padx=3,pady=3)

kl=Button(root,text="Exit",fg="white",bg="black",command=root.destroy)
kl.grid(row=6,column=2,columnspan=2,padx=3,pady=3)
ml.grid(row=8,column=0,columnspan=3)

root.mainloop()


