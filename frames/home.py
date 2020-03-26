import asyncio
import tkinter as tk
from frames.frame import *
from models.user import *
from models.printer import *

from frames.components.scrollable_frame import *
from frames.components.section import *
class Home(Frame):
  def __init__(self, parent, controller):
    Frame.__init__(self, parent, controller)

    scroll = ScrollableFrame(self)
    scroll.pack(anchor=tk.N, expand=True, fill=tk.BOTH)

    main_title = tk.Label(scroll.scrollable_frame, text = "Bienvenido", font=("Cambria",13), bg="#56CD63", fg="white", height="2")
    main_title.pack(side="top", fill="x")

    self.recent = Section(scroll.scrollable_frame, controller, title="Impresoras Recientes")
    self.recent.pack(side="top", fill="x")

    self.recommendations = Section(scroll.scrollable_frame, controller, title="Recomendaciones")
    self.recommendations.pack(side="top", fill="x")

    self.printers = Section(scroll.scrollable_frame, controller, title="Todas las impresoras", get_list=self.get_all_printers)
    self.printers.pack(side="top", fill="x")

  def menu_bar(self, root):
    menubar = tk.Menu(root)
    usermenu = tk.Menu(menubar, tearoff=0)
    usermenu.add_command(label="Salir", command=self.log_out)
    menubar.add_cascade(label="Usuario", menu=usermenu)
    return menubar

  def on_show(self, arg2):
    super()
    if arg2:
      #asyncio.ensure_future(self.recent.show_items())
      #asyncio.ensure_future(self.recommendations.show_items())
      asyncio.ensure_future(self.printers.show_items())

  async def get_all_printers(self):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, Printer.all, self.controller.user)
  
  def log_out(self):
    self.recent.clear()
    self.recommendations.clear()
    self.printers.clear()
    self.controller.log_out()