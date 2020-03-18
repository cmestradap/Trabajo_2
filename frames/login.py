import tkinter as tk
from models.user import *
from frames.frame import *

class Login(Frame):
  def __init__(self, parent, controller):
    Frame.__init__(self, parent, controller)

    email_label = tk.Label(self, text="Email", bg="#FFEEDD")
    email_label.place(x=220, y=150)
    password_label = tk.Label(self, text="Password", bg="#FFEEDD")
    password_label.place(x=220, y=210)

    self.Password = tk.StringVar()
    self.Email = tk.StringVar()

    self.email_entry = tk.Entry(self, textvariable=self.Email, width="40")
    self.password_entry = tk.Entry(self, textvariable=self.Password, width="40", show="*")

    self.email_entry.place(x=220,y=180)
    self.password_entry.place(x=220,y=240)

    login_btn = tk.Button(self, text="Ingresar", command=self.login, width="30", height="2", bg="#00CD63")
    login_btn.place(x=98, y=360)

    register_btn = tk.Button(self, text="Registrarse", command=self.register, width="30", height="2", bg="#00CD63")
    register_btn.place(x=344, y=360)

  def login(self):
    email_data = str(self.Email.get())
    password_data = str(self.Password.get())
    
    if not email_data or not password_data:
      self.show_error('Ingrese sus credenciales.')
    else:
      user = User.find(email_data)
      if user and user.verify(password_data):
        self.controller.set_user(user)
        self.email_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
      else:
        self.show_error('Credenciales invalidas.')

  def register(self):
    self.controller.show_frame("Register")