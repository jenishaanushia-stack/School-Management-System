from tkinter import*
from tkcalendar import DateEntry
from tkinter.ttk import Combobox, Treeview
from tkinter import messagebox
from datetime import date
from tkinter import ttk
import pyodbc


student_data={}
# connection between the python and sql server
def connection():
    c=pyodbc.connect(
      r'Driver={SQL Server};'
      r'Server=LAPTOP-KVDFO2KA\SQL2019;'
      r'Database=STUDENT_QUERY;'
      r'Trusted_Connection=yes;'
    )
    return c

# clearing forms after adding,updating or deleting
def clear_form():
    txt_FirstName.delete(0,END)
    txt_LastName.delete(0,END)
    txt_RegistrationNumber.delete(0,END)
    txt_PhoneNumber.delete(0,END)
    txt_Email.delete(0,END)
    txt_Gender.set("")

    
#validations that happens while adding
# Name validation
def validate_name(entry_box,event=None,show_message=True):
    name=entry_box.get().strip()
    if name =="":
        if show_message:
            messagebox.showerror("Error","Name cannot be empty")
            return False
    if not name.isalpha():
        if show_message:
            messagebox.showerror("Error","Name should contain only letters")
            return False
    if len(name)>50:
        if show_message:
            messagebox.showerror("Error","Name cannot exceed 50 characters")
            return False
    return True


#Gender validation
def validate_gender(show_message=True):
    gender=txt_Gender.get().strip()
    if gender=="":
        if show_message:
            messagebox.showerror("Eroor","Gender cannot be empty")
        return False
    return True


#DateOfBirth validation
def validate_dob(show_message=True):
    dob=txt_DateOfBirth.get_date()
    if dob>= date.today():
        if show_message:
            messagebox.showerror("Error","Date_Of_Birth is invalid")
        return False
    return True

#PhoneNumber validation
def validate_phonenumber(event=None,show_message=True):
    phone=txt_PhoneNumber.get().strip()
    if phone != "":
        if not phone.isdigit():
            if show_message:
                messagebox.showerror("Error","Phone_Number shoulld be in digits")
            return False
        if len(phone)!= 10:
            if show_message:
                messagebox.showerror("Error","Phone_Number should have 10 digits")
            return False
    return True

#Email Validation
def validate_email(event=None,show_message=True):
    email=txt_Email.get().strip()
    if email != "":
        if '@' not in email or 'gmail.com' not in email:
            if show_message:
                messagebox.showerror("Error","Email is invalid , should include @gmail.com")
            return False
        return True
    return True

# adding function for add button    
def add_data():
    
    if not validate_name(txt_FirstName):
        return
    if not validate_name(txt_LastName):
        return
    if not validate_gender():
        return
    if not validate_dob():
        return
    if not validate_phonenumber():
        return
    if not validate_email():
        return
    
    c=connection()
    cursor=c.cursor()
    fname=txt_FirstName.get().strip().lower()
    lname=txt_LastName.get().strip().lower()
    cursor.execute(""" SELECT COUNT(*) FROM STUDENTS
         WHERE LOWER(First_Name)=?
         AND LOWER(Last_Name)=?
         AND Date_Of_Birth =?""" ,(
             fname,
             lname,
             txt_DateOfBirth.get()
             ))
    count=cursor.fetchone()[0]
    if count>0:
        messagebox.showerror("Error","Student already exists with same Name and DOB")
        return
    dob = txt_DateOfBirth.get()
    gender = txt_Gender.get()

    cursor.execute(""" INSERT INTO STUDENTS
        (First_Name,Last_Name,Registration_Number,Gender,Date_Of_Birth,Phone_Number,Email)
        VALUES(?,?,?,?,?,?,?)""",(
        txt_FirstName.get(),
        txt_LastName.get(),
        txt_RegistrationNumber.get(),
        gender,
        dob,
        txt_PhoneNumber.get(),
        txt_Email.get()
    ))
    c.commit()
    load_data()
    c.close()
    print("inserted succesfully")
    clear_form()
    
#updating function for update button
    
def update_data():
    
    c=connection()
    gender=txt_Gender.get()
    dob=txt_DateOfBirth.get()
    
    cursor=c.cursor()
    cursor.execute("""UPDATE STUDENTS
        SET First_Name=?,
        Last_Name=?,
        Gender=?,
        Date_Of_Birth=?,
        Phone_Number=?,
        Email=?
        WHERE Registration_Number=?""",(
            txt_FirstName.get(),
            txt_LastName.get(),
            gender,
            dob,
            txt_PhoneNumber.get(),
            txt_Email.get(),
            txt_RegistrationNumber.get()
            ))
    c.commit()
    load_data()
    c.close()
    clear_form()

#display table function
    
def load_data():
    
    c=connection()
    cursor=c.cursor()
    cursor.execute(" SELECT First_Name,Last_Name,Registration_Number,Gender,Date_Of_Birth,Phone_Number,Email FROM STUDENTS ")
    rows=cursor.fetchall()
    tree.delete(*tree.get_children())
    for i, row in enumerate(rows):
        reg=row[2]
        student_data[reg]=row
        tag = "even" if i % 2 == 0 else "odd"
        tree.insert("",END,values=(row[0],row[1],row[2],row[4]), tags=(tag,))

    c.close()
    
#deleting function for delete button
    
def delete_data():
    c=connection()
    cursor=c.cursor()
    cursor.execute("""
        DELETE FROM STUDENTS
        WHERE Registration_Number=?""", (
            txt_RegistrationNumber.get()
            ))
    c.commit()
    load_data()
    c.close()
    clear_form()

def fill_form(event):
    selected=tree.focus()
    values=tree.item(selected,"values")
    if not values:
        return
    reg=values[2]
    data = student_data.get(reg)

    txt_FirstName.delete(0,END)
    txt_FirstName.insert(0,data[0])
    txt_LastName.delete(0,END)
    txt_LastName.insert(0,data[1])
    txt_RegistrationNumber.delete(0,END)
    txt_RegistrationNumber.insert(0,data[2])
    txt_Gender.set(data[3])
    txt_DateOfBirth.set_date(data[4])
    txt_PhoneNumber.delete(0,END)
    txt_PhoneNumber.insert(0,data[5])
    txt_Email.delete(0,END)
    txt_Email.insert(0,data[6])


# gui
def open_studentmaster():
    global window
    global txt_FirstName
    global txt_LastName
    global txt_RegistrationNumber
    global txt_Gender
    global txt_DateOfBirth
    global txt_PhoneNumber
    global txt_Email
    global tree
    global add_button

    window=Tk()
    window.title("STUDENT FORM")
    window.minsize(300,200)
    window.geometry("1000x800")

    main_frame=Frame(window,bd=5,relief="groove",background="white")
    main_frame.place(x=200,y=30,width=750,height=600)
    lbl_FirstName=Label(window,text="First_Name",font=("times of roman",10,"bold"),background="white",fg="blue")
    lbl_FirstName.place(x=300,y=100)
    txt_FirstName=Entry(window,font=("times of roman",10),width=55)
    txt_FirstName.place(x=450,y=100)
    txt_FirstName.bind("<FocusOut>",lambda event: validate_name(txt_FirstName,event, False))
    txt_FirstName.bind("<Return>", lambda event: txt_LastName.focus())

    lbl_LastName=Label(window,text="Last_Name",font=("times of roman",10,"bold"),background="white",fg="blue")
    lbl_LastName.place(x=300,y=150)
    txt_LastName=Entry(window,font=("times of roman",10),width=55)
    txt_LastName.place(x=450,y=150)
    txt_LastName.bind("<FocusOut>",lambda event: validate_name(txt_LastName,event, False))
    txt_LastName.bind("<Return>", lambda event: txt_RegistrationNumber.focus())

    lbl_RegistrationNumber=Label(window,text="Registration_Number",font=("times of roman",10,"bold"),background="white",fg="blue")
    lbl_RegistrationNumber.place(x=300,y=200)
    txt_RegistrationNumber=Entry(window,font=("times of roman",10),width=55)
    txt_RegistrationNumber.place(x=450,y=200)
    txt_RegistrationNumber.bind("<Return>", lambda event: txt_Gender.focus())

    lbl_Gender=Label(window,text="Gender",font=("times of roman",10,"bold"),background="white",fg="blue")
    lbl_Gender.place(x=300,y=250)
    txt_Gender=Combobox(window,width=62,values=["Female","Male","Others"])
    txt_Gender.place(x=450,y=250)
    txt_Gender.bind("<Return>", lambda event: txt_DateOfBirth.focus())

    lbl_DateOfBirth=Label(window,text="Date_Of_Birth",font=("times of roman",10,"bold"),background="white",fg="blue")
    lbl_DateOfBirth.place(x=300,y=300)
    txt_DateOfBirth=DateEntry(window,width=62,bg="#f5f5f5",foreground="black",borderwidth=2,date_pattern="dd/mm/yyyy")
    txt_DateOfBirth.place(x=450,y=300)
    txt_DateOfBirth.bind("<Return>", lambda event: txt_PhoneNumber.focus())

    lbl_PhoneNumber=Label(window,text="Phone_Number",font=("times of roman",10,"bold"),background="white")
    lbl_PhoneNumber.place(x=300,y=350)
    txt_PhoneNumber=Entry(window,font=("times of roman",10),width=55)
    txt_PhoneNumber.place(x=450,y=350)
    txt_PhoneNumber.bind("<FocusOut>",lambda event: validate_phonenumber(event, False))
    txt_PhoneNumber.bind("<Return>", lambda event: txt_Email.focus())

    lbl_Email=Label(window,text="Email",font=("times of roman",10,"bold"),background="white")
    lbl_Email.place(x=300,y=400)
    txt_Email=Entry(window,font=("times of roman",10),width=55)
    txt_Email.place(x=450,y=400)
    txt_Email.bind("<FocusOut>" ,lambda event: validate_email(event, False))
    txt_Email.bind("<Return>", lambda event: add_button.focus())

    # treeview
    tree=Treeview(window,show="headings")
    tree['columns']= (
        "First_Name",
        "Last_Name",
        "Registration_Number",
        "Date_Of_Birth"
        )
    style = ttk.Style()
    style.theme_use("clam")

    style.configure("Treeview",
        background="white",
        foreground="black",
        fieldbackground="white",
        rowheight=25
    )

    style.map("Treeview",
        background=[("selected", "#cce6ff")]
    )
    for col in tree["columns"]:
        tree.column(col,width=130,anchor="center")
        tree.heading(col,text=col,anchor="center")
    tree.place(x=250,y=450,width=650,height=170)
    tree.tag_configure('odd', background='white')
    tree.tag_configure('even', background='#f0f0f0')
    tree.bind("<Double-1>",fill_form)

    #button gui

    button_frame=Frame(window,bd=3,relief="groove",background="white")
    button_frame.place(x=200,y=630,width=750,height=100)
    add_button=Button(button_frame,text="Add",foreground="white",background="green",borderwidth=10,command=add_data)
    add_button.place(x=80,y=15,width=100,height=50)
    update_button=Button(button_frame,text="Update",foreground="white",background="orange",borderwidth=10,command=update_data)
    update_button.place(x=240,y=15,width=100,height=50)
    delete_button=Button(button_frame,text="Delete",foreground="white",background="red",borderwidth=10,command=delete_data)
    delete_button.place(x=400,y=15,width=100,height=50)
    close_button=Button(button_frame,text="Close",foreground="white",background="blue",borderwidth=10,command=window.destroy)
    close_button.place(x=560,y=15,width=100,height=50)
    load_data()
    txt_FirstName.focus()
    window.mainloop()


if __name__ == "__main__":
    open_studentmaster()
