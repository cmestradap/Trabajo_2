import tkinter as tk
from frames.components.item import *

class Section(tk.Frame):
  def __init__(self, parent, controller, *args, **kwargs):
    tk.Frame.__init__(self, parent)
    self.controller = controller
    self.config(background = "#213141")

    title = tk.Label(self, text=kwargs.pop('title'), font=("Cambria", 10), bg="#3b4045", fg="white", anchor='w', width=90)
    title.pack(side="top", fill="x")

    self.msg = tk.Label(self, font=("Cambria", 10), width=90, height=3)
    self.msg.pack(side="top", fill="x")

    self.grid = tk.Frame(self)
    self.grid.pack(side="top", fill="x")

    self.img = tk.PhotoImage(file='images/printer.png')
    self.get_list = kwargs.pop('get_list', None)

    self.items = []

  def clear(self):
    for item in self.items:
      item.destroy()

  async def show_items(self):
    self.msg['text'] = 'Cargando...'
    self.msg.pack(side="top", fill="x")
    self.clear()
    items = await self.get_list()
    if items:
      self.msg.pack_forget()
      for i, printer in enumerate(items):
        item = Item(self.grid, self.controller, item=printer, img=self.img)
        item.grid(column=(i % 3), row=int(i / 3), sticky="nsew", padx=(2,2), pady=(2,2))
        self.items.append(item)
    else:
      self.msg['text'] = '¡Nada que mostrar aqui!'