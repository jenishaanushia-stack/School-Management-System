from tkinter import*
from student_gui import connection
from student_gui import validate_name
from student_gui import validate_phonenumber
from tkinter.ttk import Combobox, Treeview
from tkinter import messagebox
from tkinter import ttk
selected_Guardian_Id = None
selected_Student_Id = None

# Clearing forms after adding,deleting and updating
def clear_form():
    txt_GuardianName.delete(0,END)
    txt_GuardianRelationship.delete(0,END)
    txt_GuardianPhonenumber.delete(0,END)
    txt_GuardianOccupation.delete(0,END)

# validation for registernumber combobox
def validate_combobox(entry_box, fieldname="", show_message=True):
    value = entry_box.get().strip()

    if value == "" or value.startswith("--Select"):
        if show_message:
            messagebox.showerror("Error", f"Select {fieldname}")
        return False

    return True
# adding function for add button
def add_guardiandata():
    if not validate_combobox(txt_RegistrationNumber,"Registration_Number"):
        return
    if not validate_name(txt_GuardianName,"Guardian_Name"):
        return
    if not validate_name(txt_GuardianRelationship,"Guardian_Relationship"):
        return
    if not validate_phonenumber(txt_GuardianPhonenumber,"Guardian_Phonenumber"):
        return
    if not validate_name(txt_GuardianOccupation,"Guardian_Occupation"):
        return
    c=connection()
    cursor=c.cursor()
    cursor.execute("""
    INSERT INTO Guardian
    (Student_Id,
     Guardian_Name,
     Guardian_Relationship,
     Guardian_Phonenumber,
     Guardian_Occupation)
    VALUES (?, ?, ?, ?, ?)""", 
    selected_Student_Id,
    txt_GuardianName.get(),
    txt_GuardianRelationship.get(),
    txt_GuardianPhonenumber.get(),
    txt_GuardianOccupation.get())
    c.commit()
    load_guardiandata()
    c.close()
    print("inserted succesfully")
    clear_form()
    reset_student()


# updating function for updatebutton
def update_guardiandata():
    guardian_id = tree.focus()

    if not guardian_id:
        print("Select a row first")
        return

    c = connection()
    cursor = c.cursor()

    cursor.execute("""
        UPDATE Guardian
        SET Guardian_Name=?,
            Guardian_Relationship=?,
            Guardian_Phonenumber=?,
            Guardian_Occupation=?
        WHERE Guardian_Id=?
    """, (
        txt_GuardianName.get(),
        txt_GuardianRelationship.get(),
        txt_GuardianPhonenumber.get(),
        txt_GuardianOccupation.get(),
        guardian_id
    ))

    c.commit()
    c.close()

    load_guardiandata()
    clear_form()
    reset_student()
    


# display function    
def load_guardiandata():
    c = connection()
    cursor = c.cursor()

    cursor.execute("""
        SELECT Guardian_Id,
               Guardian_Name,
               Guardian_Relationship,
               Guardian_Phonenumber,
               Guardian_Occupation
        FROM Guardian
    """)

    rows = cursor.fetchall()

    
    tree.delete(*tree.get_children())

    for index, row in enumerate(rows):
        guardian_id = str(row[0])   
        values = row[1:]

        tag = 'even' if index % 2 == 0 else 'odd'

        
        tree.insert("", END, iid=guardian_id, values=values, tags=(tag,))

    c.close()
    clear_form()
    


# deleting function for deletebutton
def delete_guardiandata():
    guardian_id = tree.focus()

    if not guardian_id:
        print("Select a row first")
        return

    c = connection()
    cursor = c.cursor()

    cursor.execute("""
        DELETE FROM Guardian
        WHERE Guardian_Id=?
    """, (guardian_id,))

    c.commit()
    c.close()

    load_guardiandata()
    clear_form()
    reset_student()
      

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
        SELECT Student_Id,First_Name, Last_Name
        FROM STUDENTS
        WHERE Registration_Number = ?
    """, (reg_no,))
    row=cursor.fetchone()
    if row:
        selected_Student_Id = row[0]
        full_name=f"{row[1]} {row[2]}"
        txt_StudentName.config(text=full_name)
    txt_GuardianName.focus()
    c.close()


# clearing the registrationnumber combobox and student display after adding,deletingand updating
def reset_student():
    global selected_Student_Id
    selected_Student_Id = None
    txt_StudentName.config(text="")
    txt_RegistrationNumber.set("--Select the Registration_Number--")
    
def fill_form(event):
    selected = tree.focus()
    values = tree.item(selected, "values")

    if not values:
        return

    global selected_Guardian_Id
    selected_Guardian_Id = selected

    txt_GuardianName.delete(0, END)
    txt_GuardianName.insert(0, values[0])

    txt_GuardianRelationship.delete(0, END)
    txt_GuardianRelationship.insert(0, values[1])

    txt_GuardianPhonenumber.delete(0, END)
    txt_GuardianPhonenumber.insert(0, values[2])

    txt_GuardianOccupation.delete(0, END)
    txt_GuardianOccupation.insert(0, values[3])
    
#gui

def open_guardianmaster():
    global window
    global txt_GuardianName
    global txt_GuardianRelationship
    global txt_GuardianPhonenumber
    global txt_GuardianOccupation
    global txt_RegistrationNumber
    global txt_StudentName
    global tree
    global add_button

    
    window=Tk()
    window.title("Guardian Table")
    window.minsize(300,200)
    window.geometry("1000x800")
    
    main_frame=Frame(window,bd=5,relief="groove",background="white")
    main_frame.place(x=200,y=100,width=750,height=560)
    
    lbl_RegistrationNumber=Label(window,text="Registration_Number",font=("times of roman",10,"bold"),background="white",foreground="blue")
    lbl_RegistrationNumber.place(x=300,y=150)
    txt_RegistrationNumber=Combobox(window,width=62)
    txt_RegistrationNumber.bind("<<ComboboxSelected>>", student_namedisplay)
    txt_RegistrationNumber.place(x=470,y=150)
    txt_RegistrationNumber.bind("<Return>", lambda event: txt_GuardianName.focus())
    load_registrationnumber()

    
    lbl_StudentName=Label(window, text="Student_Name",font=("times new roman", 10, "bold"),background="white")
    lbl_StudentName.place(x=300, y=200)
    txt_StudentName = Label(window, text="",width=55,font=("times new roman", 10, "bold"),background="white",relief="groove")
    txt_StudentName.place(x=470, y=200)

    
    lbl_GuardianName=Label(window,text="Guardian_Name",font=("times of roman",10,"bold"),background="white",foreground="blue")
    lbl_GuardianName.place(x=300,y=250)
    txt_GuardianName=Entry(window,font=("times of roman",10),width=55)
    txt_GuardianName.place(x=470,y=250)
    txt_GuardianName = Entry(window)
    txt_GuardianName.place(x=470, y=250)
    txt_GuardianName.bind("<FocusOut>",lambda event: validate_name(txt_GuardianName, "Guardian_Name",event, False))
    txt_GuardianName.bind("<Return>", lambda event: txt_GuardianRelationship.focus())


    lbl_GuardianRelationship=Label(window,text="Guardian_Relationship",font=("times of roman",10,"bold"),background="white",foreground="blue")
    lbl_GuardianRelationship.place(x=300,y=300)
    txt_GuardianRelationship=Entry(window,font=("times of roman",10),width=55)
    txt_GuardianRelationship.place(x=470,y=300)
    txt_GuardianRelationship.bind("<FocusOut>",lambda event: validate_name(txt_GuardianRelationship, "Guardian_Relationship",event, False))
    txt_GuardianRelationship.bind("<Return>", lambda event: txt_GuardianPhonenumber.focus())


    lbl_GuardianPhonenumber=Label(window,text="Guardian_PhoneNumber",font=("times of roman",10,"bold"),background="white",)
    lbl_GuardianPhonenumber.place(x=300,y=350)
    txt_GuardianPhonenumber=Entry(window,font=("times of roman",10),width=55)
    txt_GuardianPhonenumber.place(x=470,y=350)
    txt_GuardianPhonenumber.bind("<FocusOut>",lambda event: validate_phonenumber(txt_GuardianPhonenumber, "Guardian_Phonenumber",event, False))
    txt_GuardianPhonenumber.bind("<Return>", lambda event: txt_GuardianOccupation.focus())


    lbl_GuardianOccupation=Label(window,text="Guardian_Occupation",font=("times of roman",10,"bold"),background="white",foreground="blue")
    lbl_GuardianOccupation.place(x=300,y=400)
    txt_GuardianOccupation=Entry(window,font=("times of roman",10),width=55)
    txt_GuardianOccupation.place(x=470,y=400)
    txt_GuardianOccupation.bind("<FocusOut>",lambda event: validate_name(txt_GuardianOccupation, "Guardian_Occupation",event, False))


    #treeview


    tree=Treeview(window,show="headings")
    tree['columns']= (
        "Guardian_Name",
        "Guardian_Relationship",
        "Guardian_Phonenumber",
        "Guardian_Occupation")
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview",
                    background="white",
                    foreground="black",
                    fieldbackground="white",
                    rowheight=25)
    style.map("Treeview",
              background=[("selected", "#cce6ff")])
    for col in tree["columns"]:
        tree.column(col,width=130,anchor="center")
        tree.heading(col,text=col,anchor="center")
    tree.column("Guardian_Name", width=150)
    tree.column("Guardian_Relationship", width=150)
    tree.column("Guardian_Phonenumber", width=150)
    tree.column("Guardian_Occupation", width=150)
    tree.place(x=250,y=450,width=650,height=170)
    tree.tag_configure('odd', background='white')
    tree.tag_configure('even', background='#f0f0f0')
    tree.bind("<Double-1>",fill_form)


    #button gui
    
    button_frame=Frame(window,bd=3,relief="groove",background="white")
    button_frame.place(x=200,y=665,width=750,height=100)
    add_button=Button(button_frame,text="Add",background="green",foreground="white",borderwidth=10,command=add_guardiandata)
    add_button.place(x=80,y=15,width=100,height=50)
    update_button=Button(button_frame,text="Update",background="orange",foreground="white",borderwidth=10,command=update_guardiandata)
    update_button.place(x=240,y=15,width=100,height=50)
    delete_button=Button(button_frame,text="Delete",background="red",foreground="white",borderwidth=10,command=delete_guardiandata)
    delete_button.place(x=400,y=15,width=100,height=50)
    close_button=Button(button_frame,text="Close",background="blue",foreground="white",borderwidth=10,command=window.destroy)
    close_button.place(x=560,y=15,width=100,height=50)

    
    load_guardiandata()
    txt_RegistrationNumber.focus()
    
    window.mainloop()
if __name__ == "__main__":
    open_guardianmaster()

