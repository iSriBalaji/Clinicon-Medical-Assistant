import tkinter

root = tkinter.Tk()
text_widget = tkinter.Text(root,bg="#990011",fg="#FCF6F5",insertbackground="#FCF6F5",font=('Ubuntu',12,"bold"),padx=12,pady=10)
text_widget.pack(fill='both', expand=True)

text_widget.tag_configure('voice', justify='left',background="#ffd300")
text_widget.tag_configure('user', justify='right')
text_widget.insert('end',"I can help you!\n", 'voice')
text_widget.insert('end',"Thank You\n", 'user')
text_widget.insert('end',"You are perfectly alright\n", 'voice')
text_widget.insert('end',"That's great!\n", 'user')


root.mainloop()

