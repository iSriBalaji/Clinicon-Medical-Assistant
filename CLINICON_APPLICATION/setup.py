import os
from tkinter import *
from win32api import GetSystemMetrics

en_path = os.path.join(os.path.dirname(__file__),"english.py")
hi_path = os.path.join(os.path.dirname(__file__),"hindi.py")
ta_path = os.path.join(os.path.dirname(__file__),"tamil.py")

screen_width = GetSystemMetrics(0) #864
screen_height = GetSystemMetrics(1) #1536
icon_path=os.path.join(os.path.dirname(__file__),"pictures/icon.ico")

def eng():
    # with open(en_path, "rb") as source_file:
    #     code = compile(source_file.read(), "clinicon.py", "exec")
    # exec(code)
    command = r"python "+ en_path
    os.system(command)

def hin():
    command = r"python "+ hi_path
    os.system(command)

def tam():
    command = r"python "+ ta_path
    os.system(command)

if __name__ == "__main__":
    root=Tk()
    root.title("MEDILAB - Medical Data Acquisition and Analysis(Beta)")
    root.iconbitmap(icon_path)
    root.state('zoomed')
    root.configure(bg="#dae1e7")
    #root.attributes('-fullscreen', True)
    root.geometry(str(screen_width)+"x"+str(screen_height))

    constant_label=Label(root,text="MEDILAB",bg="#dae1e7",fg="#0b3a97",font=("Ubuntu",34,"bold"))
    constant_label.place(x=27,y=27)

    global lang_frame
    lang_frame = LabelFrame(root,bg="#0b3a97",relief=GROOVE)
    lang_frame.place(x=300,y=100,height=726,width=980)

    t_label=Label(lang_frame,text="Select the Language\nभाषा का चयन करें\nமொழியை தேர்ந்தெடுங்கள்",bg="#0b3a97",fg="#dae1e7",font=("Ubuntu",34,"bold"))
    t_label.pack(pady=28)

    en_next = Button(lang_frame,text="English",bg="#158dd4",fg="#ffffff",font=("Ubuntu",21,"bold"),padx=287,pady=20,command=eng)
    en_next.pack(pady=12)
    hi_next = Button(lang_frame,text="हिन्दी",bg="#158dd4",fg="#ffffff",font=("Ubuntu",21,"bold"),padx=302,pady=20,command=hin)
    hi_next.pack(pady=12)
    tn_next = Button(lang_frame,text="தமிழ்",bg="#158dd4",fg="#ffffff",font=("Ubuntu",21,"bold"),padx=287,pady=20,command=tam)
    tn_next.pack(pady=12)

    root.mainloop()



