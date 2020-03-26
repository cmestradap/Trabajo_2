import tkinter as tk
import math

class Star(tk.Label):
  def __init__(self, master=None, index=0, cnf={}, **kw):
    tk.Label.__init__(self, master, cnf, **kw)
    self.index = index

class Rating(tk.Frame):
  def __init__(self, parent, controller, *args, **kwargs):
    tk.Frame.__init__(self, parent)
    self.controller = controller

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
    prev = None
    for i in range(0, 5):
      star = Star(self, i, image=self.empty, bg=bgcolor)
      star.image = self.empty
      star.grid(row=0, column=i, sticky="nsew")
      if view:
        star.bindtags((view,) + star.bindtags())
      else:
        star.bind("<Button-1>", self.__on_click)

      self.stars.append(star)
      prev = star

    self.set_item(kwargs.pop('item', None))

  def set_bg_color(self, color):
    for star in self.stars:
      star.configure(background=color)

  def set_item(self, item):
    self.item = item

    if item:
      fra, dec = math.modf(item.rating)

      dec = int(dec)
      self.__set_stars(dec)
      if dec < 5:
        if fra > 0.5:
          self.__change_img(self.stars[dec], self.full)
        elif fra > 0.0:
          self.__change_img(self.stars[dec], self.half)
        else:
          self.__change_img(self.stars[dec], self.empty)

  def __on_click(self, event):
    star = event.widget
    w = star.winfo_width() / 2
    q = star.index
    if event.x >= w:
      self.__change_img(star, self.full)
      q += 1.0
    else:
      self.__change_img(star, self.half)
      q += 0.5

    self.__set_stars(star.index)
    if self.item.rate(q, self.controller.user):
      self.event_generate('<<Rating>>', when='tail')

  def __set_stars(self, index):
    for p in range(0, index):
      self.__change_img(self.stars[p], self.full)

    if index < 5:
      for p in range(index + 1, 5):
        self.__change_img(self.stars[p], self.empty)

  def __change_img(self, star, img):
    star.configure(image=img)
    star.image = img