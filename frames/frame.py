import tkinter as tk

class Frame(tk.Frame):
  def __init__(self, parent, controller):
    tk.Frame.__init__(self, parent)
    self.controller = controller
    self.config(background = "#213141")

    self.error_msg = tk.Label(self, text="Example", font=("Cambria",10), bg="#dc3545", fg="white", width="550", height="2")
    self.error_msg.pack_forget()

  def menu_bar(self, root):
    return ""

  def show_error(self, msg):
    self.error_msg['text'] = msg
    self.error_msg.pack()

  def hide_error(self):
    self.error_msg.pack_forget()