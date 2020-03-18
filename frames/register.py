import tkinter as tk
from models.user import *
from frames.frame import *

class Register(Frame):
  def __init__(self, parent, controller):
    Frame.__init__(self, parent, controller)

    main_title = tk.Label(self, text = "Registro de Usuarios", font=("Cambria",13), bg="#56CD63", fg="white", width="550", height="2")
    main_title.pack()

    username_label = tk.Label(self, text="Username", bg="#FFEEDD")
    username_label.place(x=220, y=150)
    password_label = tk.Label(self, text="Password", bg="#FFEEDD")
    password_label.place(x=220, y=210)
    email_label = tk.Label(self, text="E-mail", bg="#FFEEDD")
    email_label.place(x=220, y=270)

    self.Username = tk.StringVar()
    self.Password = tk.StringVar()
    self.Email = tk.StringVar()

    self.username_entry = tk.Entry(self, textvariable=self.Username, width="40")
    self.password_entry = tk.Entry(self, textvariable=self.Password, width="40", show="*")
    self.email_entry = tk.Entry(self, textvariable=self.Email, width="40")

    self.username_entry.place(x=220,y=180)
    self.password_entry.place(x=220,y=240)
    self.email_entry.place(x=220,y=300)

    login_btn = tk.Button(self, text="Registrar", command=self.send_data, width="30", height="2", bg="#00CD63")
    login_btn.place(x=98, y=360)

    register_btn = tk.Button(self, text="Atras", command=self.go_back, width="30", height="2", bg="#00CD63")
    register_btn.place(x=344, y=360)

  def send_data(self):
    username_data = self.Username.get()
    password_data = str(self.Password.get())
    email_data = str(self.Email.get())

    if not username_data or not password_data or not email_data:
      self.show_error('Todos los campos son requeridos.')
    else:
      user = User.create(username_data, email_data, password_data)
      if user.insert():
        self.go_back()
      else:
        self.show_error('No se pudo registrar, revise sus datos e intente mas tarde.')

  def go_back(self):
    self.username_entry.delete(0, tk.END)
    self.password_entry.delete(0, tk.END)
    self.email_entry.delete(0, tk.END)
    
    self.controller.show_frame("Login")