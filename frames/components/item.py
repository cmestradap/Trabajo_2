import tkinter as tk
from frames.components.rating import *

class Item(tk.Frame):
  def __init__(self, parent, controller, *args, **kwargs):
    tk.Frame.__init__(self, parent)
    self.controller = controller
    item = kwargs.pop('item')
    self.item = item
  
    img = kwargs.pop('img')
    image = tk.Label(self, image=img)
    image.image = img
    image.grid(row=0, column=0, rowspan=5, sticky="nsew", padx=(5, 5))

    model = tk.Label(self, text=item.model, anchor='w')
    model.grid(row=0,column=1, sticky=tk.W)

    price = tk.Label(self, text=f"${item.price}", anchor='e')
    price.grid(row=0, column=2, sticky=tk.W)

    color = tk.Label(self, text=f"Color: {item.color}", anchor='w')
    color.grid(row=1, column=1, columnspan=2, sticky="nsew")

    scanner = tk.Label(self, text=f"Escaner: {item.scanner}", anchor='w')
    scanner.grid(row=2, column=1, columnspan=2, sticky="nsew")

    wifi = tk.Label(self, text=f"Wifi: {item.wifi}", anchor='w')
    wifi.grid(row=3, column=1, columnspan=2, sticky="nsew")

    class_name = f"i{item.id}"
    rating_item = item.rating()
    self.rating = None
    if rating_item:
      self.rating = Rating(self, controller, item=rating_item, bg="white", view=class_name)
      self.rating.grid(row=4, column=0, columnspan=3, sticky="nsew", pady=(5,5))

    for widget in (self, *self.winfo_children()):
      widget.bindtags((class_name,) + widget.bindtags())

    self.bind_class(class_name, "<Button>", lambda event: controller.show_frame("Printer", item))
    self.bind("<Enter>", self.__on_enter)
    self.bind("<Leave>", self.__on_leave)
    self.__change_bg('white')
    
  def __on_enter(self, event):
    self.__change_bg('#e1ecf4')

  def __on_leave(self, event):
    self.__change_bg('white')

  def __change_bg(self, color):
    self.configure(background=color)
    if self.rating:
      self.rating.set_bg_color(color)
    for child in self.winfo_children():
      child.configure(background=color)