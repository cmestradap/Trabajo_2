import tkinter as tk
from models.user import *
from frames.frame import *

class Profile(Frame):
  def __init__(self, parent, controller):
    Frame.__init__(self, parent, controller)

    main_title = tk.Label(self, text = "Perfil de Usuario", font=("Cambria",13), bg="#56CD63", fg="white", height="2")
    main_title.pack(side="top", fill="x")

    self.data = tk.Label(self, font=("Cambria",13), bg="#213141", fg="white")
    self.data.pack(side="top", fill="x")
    self.columns = None
    self.values = None

  def menu_bar(self, root):
    menubar = tk.Menu(root)
    usermenu = tk.Menu(menubar, tearoff=0)
    usermenu.add_command(label="Inicio", command=self.home)
    usermenu.add_command(label="Salir", command=self.log_out)
    menubar.add_cascade(label="Usuario", menu=usermenu)
    return menubar

  def set_profile_model(self, columnaPerfilUser, valorPerfilUser):
    print(columnaPerfilUser)
    print(valorPerfilUser)

    self.columns = columnaPerfilUser
    self.values = valorPerfilUser

  def home(self):
    self.controller.show_frame("Home")
  
  def log_out(self):
    self.controller.log_out()

  def on_show(self, arg2):
    super()
    user = self.controller.user

    data = ""
    if self.columns:
      for i in range(0, len(self.columns)):
        data += f"{self.columns[i]}: {self.values[i]}\n"

    self.data['text'] = f"Nombre: {user.name}\nCorreo: {user.email}\n{data}"