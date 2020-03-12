from tkinter import *
from models.user import User

def send_data():
  username_data = Username.get()
  password_data = str(Password.get())
  Email_data = str(Email.get())

  user = User.create(username_data, Email_data, password_data)
  user.insert()
  print(username_data, "\t", password_data, "\t", Email_data)

  username_entry.delete(0,END)
  password_entry.delete(0,END)
  email_entry.delete(0,END)

mywindow = Tk()
ancho = mywindow.winfo_screenwidth()
alto = mywindow.winfo_screenheight()
print(ancho, " ",alto)
mywindow.geometry("650x550")
mywindow.title("Formulario de Registro")
mywindow.resizable(False,False)
mywindow.config(background = "#213141")
main_title = Label (text = "Registro de Usuarios", font=("Cambria",13), bg="#56CD63", fg="white", width="550", height="2")
main_title.pack()

username_label = Label(text="Username", bg="#FFEEDD")
username_label.place(x=220, y=150)
password_label = Label(text="Password", bg="#FFEEDD")
password_label.place(x=220, y=210)
email_label = Label(text="E-mail", bg="#FFEEDD")
email_label.place(x=220, y=270)

Username = StringVar()
Password = StringVar()
Email = StringVar()

username_entry = Entry(textvariable=Username, width="40")
password_entry = Entry(textvariable=Password, width="40", show="*")
email_entry = Entry(textvariable=Email, width="40")

username_entry.place(x=220,y=180)
password_entry.place(x=220,y=240)
email_entry.place(x=220,y=300)

submit_btn = Button(mywindow, text="Registrar", command=send_data, width="30", height="2", bg="#00CD63")
submit_btn.place(x=230, y=360)

mywindow.mainloop()