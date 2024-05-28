import tkinter as tk
from tkinter import * 
from tkinter import font as tkFont
import tkinter.font as tkf

root = tk.Tk()
print(tkf.families())
default_font = tkFont.nametofont("TkDefaultFont")
root.option_add("Ubuntu", default_font)
lab=Label(root,text="Hello Dudenjklke")
lab.pack()
lab1=Label(root,text="Hello Dudenjklke",font=("Ubuntu",20))
lab1.pack()
root.mainloop()

