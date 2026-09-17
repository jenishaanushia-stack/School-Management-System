from tkinter import*
from tkinter.ttk import Combobox
from tkinter import ttk
from tkinter.ttk import Treeview
from Guardian_gui import validate_combobox
from tkinter import messagebox
from student_gui import connection
selected_Student_Id = None
loaded_mark_ids = []


#validation for mark
def validate_mark(entry_box,field_name="",event=None,show_message=True):
    mark=entry_box.get()
    if mark =="":
        if show_message:
            messagebox.showerror("Error",f"{field_name} cannot be empty")
            return False
    if not mark.isdigit():
        if show_message:
            messagebox.showerror("Error",f"{field_name} should contain only digits")
            return False
    return True

#validation for duplicate subjects
def validate_subjects():
    subjects = [
        txt_subject1.get(),
        txt_subject2.get(),
        txt_subject3.get(),
        txt_subject4.get(),
        txt_subject5.get()
    ]

    if len(subjects) != len(set(subjects)):
        messagebox.showerror("Error", "Duplicate subjects are not allowed")
        return False

    return True



# Clearing forms after adding,deleting and updating
def clear_form():
    txt_subject1.set("--Select Subject--")
    txt_subject2.set("--Select Subject--")
    txt_subject3.set("--Select Subject--")
    txt_subject4.set("--Select Subject--")
    txt_subject5.set("--Select Subject--")

    txt_mark1.delete(0, END)
    txt_mark2.delete(0, END)
    txt_mark3.delete(0, END)
    txt_mark4.delete(0, END)
    txt_mark5.delete(0, END)

    txt_semester.set("--Select Semester--")

    txt_mark1.focus()



# adding function for add button
def add_markdata():
    global selected_Student_Id
    if not validate_combobox(txt_RegistrationNumber,"Registration_Number"):
        return
    if not validate_combobox(txt_subject1,"Subject"):
        return
    if not validate_mark(txt_mark1,"mark"):
        return
    if not validate_combobox(txt_subject2,"Subject"):
        return
    if not validate_mark(txt_mark2,"mark"):
        return
    if not validate_combobox(txt_subject3,"Subject"):
        return
    if not validate_mark(txt_mark3,"mark"):
        return
    if not validate_combobox(txt_subject4,"Subject"):
        return
    if not validate_mark(txt_mark4,"mark"):
        return
    if not validate_combobox(txt_subject5,"Subject"):
        return
    if not validate_mark(txt_mark5,"mark"):
        return
    if not validate_subjects():
        return
    c=connection()
    cursor=c.cursor()
    Semester = txt_semester.get()
    subject_mark=[ (txt_subject1.get(),txt_mark1.get()),
               (txt_subject2.get(),txt_mark2.get()),
                   (txt_subject3.get(),txt_mark3.get()),
                   (txt_subject4.get(),txt_mark4.get()),
                   (txt_subject5.get(),txt_mark5.get())
        ]
    for Display_order , (Subject,Mark )in enumerate(subject_mark,start=1):
        cursor.execute(""" INSERT INTO Mark (Student_Id,Subject,Mark,Semester,Display_order)
VALUES(?,?,?,?,?)""",(selected_Student_Id,Subject,Mark,Semester,Display_order))
    c.commit()
    load_markdata()
    clear_form()
    reset_student()
    c.close()



# updating function for updatebutton   
def update_markdata():
    global loaded_mark_ids

    c = connection()
    cursor = c.cursor()

    semester = txt_semester.get()

    subject_mark = [
        (txt_subject1.get(), txt_mark1.get()),
        (txt_subject2.get(), txt_mark2.get()),
        (txt_subject3.get(), txt_mark3.get()),
        (txt_subject4.get(), txt_mark4.get()),
        (txt_subject5.get(), txt_mark5.get())
    ]

    for display_order, (mark_id, (subject, mark)) in enumerate(
            zip(loaded_mark_ids, subject_mark), start=1):

        cursor.execute("""
            UPDATE Mark
            SET Subject=?,
                Mark=?,
                Semester=?,
                Display_Order=?
            WHERE Mark_Id=?
        """,
        (
            subject,
            mark,
            semester,
            display_order,
            mark_id
        ))

    c.commit()
    c.close()

    load_markdata()
    clear_form()
    reset_student()



# display function  
def load_markdata():

    if selected_Student_Id is None:
        return

    c = connection()
    cursor = c.cursor()

    cursor.execute("""
        SELECT Mark_Id,
               Subject,
               Mark,
               Semester,
               Display_Order
        FROM Mark
        WHERE Student_Id = ?
        ORDER BY Display_Order
    """, (selected_Student_Id,))

    rows = cursor.fetchall()

    tree.delete(*tree.get_children())

    for index, row in enumerate(rows):

        tag = "even" if index % 2 == 0 else "odd"

        tree.insert(
            "",
            END,
            iid=str(row[0]),
            values=(
                row[1], 
                row[2],  
                row[3]   
            ),
            tags=(tag,)
        )

    c.close()



    
def fill_form(event):
    global selected_Student_Id, loaded_mark_ids

    selected = tree.focus()
    values = tree.item(selected, "values")

    if not values:
        return

    semester = values[2]

    c = connection()
    cursor = c.cursor()

    cursor.execute("""
        SELECT Mark_Id,
               Subject,
               Mark
        FROM Mark
        WHERE Student_Id = ?
        AND Semester = ?
        ORDER BY Display_Order
    """, (selected_Student_Id, semester))

    rows = cursor.fetchall()

    loaded_mark_ids.clear()

    subjects = [txt_subject1, txt_subject2, txt_subject3, txt_subject4, txt_subject5]
    marks = [txt_mark1, txt_mark2, txt_mark3, txt_mark4, txt_mark5]

    for subject_box in subjects:
        subject_box.set("--Select Subject--")

    for mark_box in marks:
        mark_box.delete(0, END)

    for i, row in enumerate(rows):
        loaded_mark_ids.append(row[0])

        subjects[i].set(row[1])

        marks[i].delete(0, END)
        marks[i].insert(0, row[2])

    txt_semester.set(semester)

    c.close()



# to display the registernumber in the combobox
def load_registrationnumber():
    c=connection()
    cursor=c.cursor()
    cursor.execute(""" SELECT Registration_Number from STUDENTS """)
    rows = cursor.fetchall()
    reg_number=[]
    for row in rows:
        reg_number.append(row[0])
    txt_RegistrationNumber["values"]=reg_number
    txt_RegistrationNumber.set("--Select the Registration_Number--")
    c.close()




# displaying the studentname  
def student_namedisplay(event):
    global selected_Student_Id

    c = connection()
    cursor = c.cursor()

    reg_no = txt_RegistrationNumber.get()

    cursor.execute("""
        SELECT Student_Id,
               First_Name,
               Last_Name
        FROM STUDENTS
        WHERE Registration_Number = ?
    """, (reg_no,))

    row = cursor.fetchone()

    if row:
        selected_Student_Id = row[0]

        full_name = f"{row[1]} {row[2]}"
        txt_StudentName.config(text=full_name)

        load_markdata()

    c.close()


    
# deleting function for deletebutton
def delete_markdata():
    mark_id = tree.focus()

    if not mark_id:
        print("Select a row first")
        return

    c = connection()
    cursor = c.cursor()

    cursor.execute("""
        DELETE FROM Mark
        WHERE Mark_Id = ?
    """, (mark_id,))

    c.commit()
    load_markdata()
    clear_form()
    c.close()

    load_markdata()
    clear_form()
    reset_student()



# clearing the registrationnumber combobox and student display after adding,deletingand updating
def reset_student():
    global selected_Student_Id
    selected_Student_Id = None
    txt_StudentName.config(text="")
    txt_RegistrationNumber.set("--Select the Registration_Number--")
    


def open_markmaster():
    global txt_RegistrationNumber
    global txt_StudentName
    global txt_subject1
    global txt_subject2
    global txt_subject3
    global txt_subject4
    global txt_subject5
    global txt_mark1
    global txt_mark2
    global txt_mark3
    global txt_mark4
    global txt_mark5
    global txt_semester
    global tree


    #gui
    window=Tk()
    window.title("Marks")
    window.minsize(300,200)
    window.geometry("1000x800")

    
    main_frame=Frame(window,bd=5,relief="groove",background="white")
    main_frame.place(x=100,y=30,width=850,height=620)

    
    lbl_RegistrationNumber=Label(window,text="Registration_Number",font=("times of roman",10,"bold"),background="white")
    lbl_RegistrationNumber.place(x=200,y=50)
    txt_RegistrationNumber=Combobox(window,width=62)
    txt_RegistrationNumber.bind("<<ComboboxSelected>>", student_namedisplay)
    load_registrationnumber()
    txt_RegistrationNumber.place(x=500,y=50)
    txt_RegistrationNumber.bind("<Return>", lambda event: txt_subject1.focus())

    
    lbl_StudentName=Label(window, text="Student_Name",font=("times new roman", 10, "bold"),background="white")
    lbl_StudentName.place(x=200, y=100)
    txt_StudentName = Label(window, text="",width=55,font=("times new roman", 10, "bold"),background="white",relief="groove")
    txt_StudentName.place(x=500, y=100)

    
    txt_subject1=Combobox(window,width=35,values=["C++","MATH","PHY","EEE","ENG"])
    txt_subject1.place(x=200,y=150)
    txt_subject1.set("--Select Subject--")
    txt_mark1=Entry(window,width=55,font=("times of roman",10),justify="center")
    txt_mark1.place(x=500,y=150)
    txt_mark1.bind("<Return>", lambda event: txt_mark2.focus())

    
    txt_subject2=Combobox(window,width=35,values=["C++","MATH","PHY","EEE","ENG"])
    txt_subject2.place(x=200,y=200)
    txt_subject2.set("--Select Subject--")
    txt_mark2=Entry(window,width=55,font=("times of roman",10),justify="center")
    txt_mark2.place(x=500,y=200)
    txt_mark2.bind("<Return>", lambda event: txt_mark3.focus())

    
    txt_subject3=Combobox(window,width=35,values=["C++","MATH","PHY","EEE","ENG"])
    txt_subject3.place(x=200,y=250)
    txt_subject3.set("--Select Subject--")
    txt_mark3=Entry(window,width=55,font=("times of roman",10),justify="center")
    txt_mark3.place(x=500,y=250)
    txt_mark3.bind("<Return>", lambda event: txt_mark4.focus())

    
    txt_subject4=Combobox(window,width=35,values=["C++","MATH","PHY","EEE","ENG"])
    txt_subject4.place(x=200,y=300)
    txt_subject4.set("--Select Subject--")
    txt_mark4=Entry(window,width=55,font=("times of roman",10),justify="center")
    txt_mark4.place(x=500,y=300)
    txt_mark4.bind("<Return>", lambda event: txt_mark5.focus())

    
    txt_subject5=Combobox(window,width=35,values=["C++","MATH","PHY","EEE","ENG"])
    txt_subject5.place(x=200,y=350)
    txt_subject5.set("--Select Subject--")
    txt_mark5=Entry(window,width=55,font=("times of roman",10),justify="center")
    txt_mark5.place(x=500,y=350)

    
    txt_semester=Combobox(window,width=110,values=["1","2","3","4","5","6","7","8"])
    txt_semester.configure(justify="center")
    txt_semester.place(x=200,y=400)
    txt_semester.set("--Select Semester--")


    #treeview
    tree = Treeview(window, show="headings")
    tree["columns"] = (
        "Subject",
        "Mark",
        "Semester"
        )
    style = ttk.Style()
    style.theme_use("clam")
    style.configure(
        "Treeview",
        background="white",
        foreground="black",
        fieldbackground="white",
        rowheight=25
        )
    style.map(
        "Treeview",
        background=[("selected", "#cce6ff")]
        )
    for col in tree["columns"]:
        tree.column(col, width=150, anchor="center")
        tree.heading(col, text=col, anchor="center")
    tree.place(x=150, y=450, width=750, height=180)
    tree.tag_configure('odd', background='white')
    tree.tag_configure('even', background='#f0f0f0')
    tree.bind("<Double-1>", fill_form)


    #buttongui
    button_frame=Frame(window,bd=3,relief="groove",background="white")
    button_frame.place(x=100,y=650,width=850,height=100)
    add_button=Button(button_frame,text="Add",background="green",foreground="white",borderwidth=10,command=add_markdata)
    add_button.place(x=50,y=15,width=100,height=50)
    update_button=Button(button_frame,text="Update",background="orange",foreground="white",borderwidth=10,command=update_markdata)
    update_button.place(x=250,y=15,width=100,height=50)
    delete_button=Button(button_frame,text="Delete",background="red",foreground="white",borderwidth=10,command=delete_markdata)
    delete_button.place(x=450,y=15,width=100,height=50)
    close_button=Button(button_frame,text="Close",background="blue",foreground="white",borderwidth=10,command=window.destroy)
    close_button.place(x=650,y=15,width=100,height=50)

    
    txt_mark1.focus()
    window.mainloop()
if __name__ == "__main__":
    open_markmaster()
    
