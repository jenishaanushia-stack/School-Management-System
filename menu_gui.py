from tkinter import*
from student_gui import open_studentmaster
from Guardian_gui import open_guardianmaster
from marks_gui import open_markmaster


root=Tk()
root.title("Student Management System")
root.geometry("400x300")
menubar=Menu(root)
file_menu=Menu(menubar,tearoff=0)
file_menu.add_command(label="Student",command=open_studentmaster)
file_menu.add_command(label="Guardian",command=open_guardianmaster)
file_menu.add_command(label="Marks",command=open_markmaster)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.destroy)
menubar.add_cascade(label="Master",menu=file_menu)
root.config(menu=menubar)
file_menu1=Menu(menubar,tearoff=0)
file_menu1.add_command(label="Results")
menubar.add_cascade(label="Report",menu=file_menu1)
root.configure(bg="#EAF4FF")
title=Label(root,text="Student Management System",font=("georgia",38,"bold italic"),bg="#EAF4FF",fg="#003A99")
title.place(x=770,y=350,anchor="center")


root.mainloop()

