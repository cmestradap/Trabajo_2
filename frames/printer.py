import tkinter as tk
from models.user import *
from frames.frame import *
from frames.components.rating import *
import webbrowser

def callback(url):
  if url:
    webbrowser.open_new(url)

class Printer(Frame):
  def __init__(self, parent, controller):
    Frame.__init__(self, parent, controller)

    header = tk.Frame(self, width=90)
    header.pack(side="top", fill="x")

    img = tk.PhotoImage(file='images/back arrow.png')
    image = tk.Button(header, image=img, command=self.go_back)
    image.image = img
    image.grid(row=0, column=0, sticky="w", pady=(0, 10))

    ptr = tk.PhotoImage(file="images/printer.png")
    icon = tk.Label(header, image=ptr)
    icon.image = ptr
    icon.grid(row=1, column=0, rowspan=4, sticky="nsew", padx=(15, 0))

    self.title = tk.Label(header, width=50)
    self.title.grid(row=0, column=1, columnspan=3, sticky="nsew", pady=(0, 10))

    price_tag = tk.Label(header, text="Price:")
    price_tag.grid(row=1, column=1, sticky="e")
    self.price = tk.Label(header)
    self.price.grid(row=1, column=2, sticky="w")

    color_tag = tk.Label(header, text="Color:")
    color_tag.grid(row=2, column=1, sticky="e")
    self.color = tk.Label(header)
    self.color.grid(row=2, column=2, sticky="w")

    scanner_tag = tk.Label(header, text="Escaner:")
    scanner_tag.grid(row=3, column=1, sticky="e")
    self.scanner = tk.Label(header)
    self.scanner.grid(row=3, column=2, sticky="w")

    wifi_tag = tk.Label(header, text="Wifi:")
    wifi_tag.grid(row=4, column=1, sticky="e")
    self.wifi = tk.Label(header)
    self.wifi.grid(row=4, column=2, sticky="w")

    self.link1 = tk.StringVar()
    link1_tag = tk.Label(header, text="Link 1:")
    link1_tag.grid(row=5, column=0, sticky="ne")
    link1_val = tk.Label(header, textvariable=self.link1, width=80, wraplength=510, fg="blue", cursor="hand2", anchor="w")
    link1_val.grid(row=5, column=1, columnspan=3, sticky="w")
    link1_val.bind("<Button-1>", lambda e: callback(self.link1.get()))
    
    self.link2 = tk.StringVar()
    link2_tag = tk.Label(header, text="Link 2:")
    link2_tag.grid(row=6, column=0, sticky="ne")
    link2_val = tk.Label(header, textvariable=self.link2, width=80, wraplength=510, fg="blue", cursor="hand2", anchor="w")
    link2_val.grid(row=6, column=1, columnspan=3, sticky="w")
    link2_val.bind("<Button-1>", lambda e: callback(self.link2.get()))

    obs_tag = tk.Label(header, text="Observaciones:")
    obs_tag.grid(row=7, column=0, sticky="ne")
    self.obs = tk.Label(header, width=80, wraplength=510, anchor="w")
    self.obs.grid(row=7, column=1, columnspan=3, sticky="w")

    rating_tag = tk.Label(header, text="Calificación:")
    rating_tag.grid(row=8, column=0, sticky="ne")
    self.rating = Rating(header, controller, item=None)
    self.rating.grid(row=8, column=1, columnspan=2, sticky="w")

  def on_show(self, arg2):
    super()
    self.title['text'] = arg2.model
    self.price['text'] = f"${arg2.price}"
    self.color['text'] = arg2.color
    self.scanner['text'] = arg2.scanner
    self.wifi['text'] = arg2.wifi
    self.link1.set(arg2.link1)
    self.link2.set(arg2.link2)
    self.obs['text'] = arg2.observations

  def go_back(self):
    self.controller.show_frame("Home", False) #Set if changed