import tkinter as tk

class Rating(tk.Frame):
  def __init__(self, parent, controller, *args, **kwargs):
    tk.Frame.__init__(self, parent)
    self.controller = controller
    self.item = kwargs.pop('item')

    view = kwargs.pop('view', False)
    if view:
      self.full = tk.PhotoImage(file='images/full_sm.png')
      self.half = tk.PhotoImage(file='images/half_sm.png')
      self.empty = tk.PhotoImage(file='images/empty_sm.png')
      self.bindtags((self,) + self.bindtags())
    else:
      self.full = tk.PhotoImage(file='images/full.png')
      self.half = tk.PhotoImage(file='images/half.png')
      self.empty = tk.PhotoImage(file='images/empty.png')

    self.stars = []
    bgcolor = kwargs.pop('bg', None)
    for i in range(0, 5):
      star = tk.Label(self, image=self.empty, bg=bgcolor)
      star.image = self.empty
      star.grid(row=0, column=i, sticky="nsew")
      if view:
        star.bindtags((view,) + star.bindtags())
      self.stars.append(star)

  def set_bg_color(self, color):
    for star in self.stars:
      star.configure(background=color)