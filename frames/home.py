import tkinter as tk
from frames.frame import *
from models.user import *

class Home(Frame):
  def __init__(self, parent, controller):
    Frame.__init__(self, parent, controller)

    main_title = tk.Label(self, text = "Bienvenido", font=("Cambria",13), bg="#56CD63", fg="white", width="550", height="2")
    main_title.pack()

  def menu_bar(self, root):
    menubar = tk.Menu(root)
    usermenu = tk.Menu(menubar, tearoff=0)
    usermenu.add_command(label="Salir", command=self.log_out)
    menubar.add_cascade(label="Usuario", menu=usermenu)
    return menubar

  def log_out(self):
    self.controller.log_out()