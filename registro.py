from tkinter import *

mywindow = Tk();
mywindow.geometry("650x550")
mywindow.title("Registration Form")
mywindow.resizable(False,False)
mywindow.config(background = "#213141")
main_title = Label (text = "Registro de Usuarios", font=("Cambria",13), bg="#56CD63", fg="white", width="550", height="2")
main_title.pack()

username_label = Label(text="Username", bg="#FFEEDD")
username_label.place(x=22, y=70)
password_label = Label(text="Password", bg="#FFEEDD")
password_label.place(x=22, y=130)
email_label = Label(text="E-mail", bg="#FFEEDD")
email_label.place(x=22, y=190)

username_entry = Entry(textvariable=username, width="40")
password_entry = Entry(textvariable=password, width="40")
email_entry = Entry(textvariable=email, width="40")