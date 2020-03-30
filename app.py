import asyncio
import tkinter as tk
from frames.register import *
from frames.login import *
from frames.home import *
from frames.printer import *
from frames.profile import *

class App(tk.Tk):
  def __init__(self, *args, **kwargs):
    tk.Tk.__init__(self, *args, **kwargs)
    self.geometry("650x550")
    self.resizable(False,False)
    
    self.container = tk.Frame(self)
    self.container.pack(side="top", fill="both", expand=True)
    self.container.grid_rowconfigure(0, weight=1)
    self.container.grid_columnconfigure(0, weight=1)
    
    self.user = None
    self.frames = {}
    self.menus = {}
    self.register_frame(Login)
    self.register_frame(Register)
    self.register_frame(Home)
    self.register_frame(Printer)
    self.register_frame(Profile)

    self.show_frame("Login")

  def register_frame(self, F):
    page_name = F.__name__
    frame = F(parent=self.container, controller=self)
    frame.grid(row=0, column=0, sticky="nsew")
    self.frames[page_name] = frame
    self.menus[page_name] = frame.menu_bar(self)

  def show_frame(self, page_name, arg2 = None):
    frame = self.frames[page_name]
    frame.on_show(arg2)
    frame.tkraise()

    menubar = self.menus[page_name]
    self.configure(menu=menubar)

  def set_user(self, user):
    self.user = user
    self.show_frame("Home", True)

  def log_out(self):
    self.user = None
    self.show_frame("Login")

async def run_tk(root):
  try:
    while True:
      root.update()
      await asyncio.sleep(.01)
  except tk.TclError as e:
    if "application has been destroyed" not in e.args[0]:
      raise

if __name__ == '__main__':
  app = App()
  asyncio.get_event_loop().run_until_complete(run_tk(app))