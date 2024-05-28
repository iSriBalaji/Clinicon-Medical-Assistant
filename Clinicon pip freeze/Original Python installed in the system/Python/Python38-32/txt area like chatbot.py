from tkinter import *
import tkinter as tk
import os
from PIL import ImageTk
import PIL.Image as pl


root=Tk()
assistant_Area = Text(root,bg="#990011",fg="#FCF6F5",insertbackground="#FCF6F5",font=('Ubuntu',12,"bold"),padx=12,pady=10)
assistant_Area.grid(row=0,column=0)
assistant_Area.insert(END,"Baju: I'm Baju, A in-bulit Voice Assistant in CLINICON\n")
assistant_Area.insert(END,"Baju: I can help you with Diagnosing\n")

img=ImageTk.PhotoImage(pl.open(os.path.join(os.path.dirname(__file__),"world.gif")))
assistant_Area.image_create(tk.END, image = img)
root.mainloop()


#to align left and right
##text_widget.tag_configure('voice', justify='left')
##text_widget.tag_configure('user', justify='right')
##text_widget.insert('end',"I can help you!\n", 'voice')
##text_widget.insert('end',"Thank You\n", 'user')
##text_widget.insert('end',"You are perfectly alright\n", 'voice')
##text_widget.insert('end',"That's great!\n", 'user')
