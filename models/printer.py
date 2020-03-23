import psycopg2
from database import cursor, connection

class Printer:
  def __init__(self, id, model, color, wifi, scanner, price, observations, link1, link2):
    self.id = id
    self.model = model
    self.color = color
    self.wifi = wifi
    self.scanner = scanner
    self.price = price
    self.observations = observations
    self.link1 = link1
    self.link2 = link2

  def rating(self):
    return None

  @classmethod
  def all(cls):
    cursor.execute("SELECT id, modelo, tipo_color, wifi, escaner, precio, observaciones, link1, link2 FROM impresoras")
    return [cls(*record) for record in cursor.fetchall()]