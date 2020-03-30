from database import cursor, connection
from models.rating import *

class Printer:
  def __init__(self, id, model, color, wifi, scanner, price, observations, link1, link2, r_id, user_id, printer_id, rating, created_at, updated_at):
    self.id = id
    self.model = model
    self.color = color
    self.wifi = wifi
    self.scanner = scanner
    self.price = price
    self.observations = observations
    self.link1 = link1
    self.link2 = link2

    printer = printer_id if printer_id else id
    self.rating = Rating(r_id, user_id, printer, rating, created_at, updated_at)

  @classmethod
  def all(cls, user):
    cursor.execute("SELECT impresoras.id, modelo, tipo_color, wifi, escaner, precio, observaciones, link1, link2, calificaciones.id, calificaciones.user_id, calificaciones.impresora_id, calificaciones.calificacion, calificaciones.created_at, calificaciones.updated_at FROM impresoras LEFT OUTER JOIN calificaciones ON calificaciones.impresora_id = impresoras.id AND calificaciones.user_id = %s", (user.id,))
    return [cls(*record) for record in cursor.fetchall()]

  @classmethod
  def recents(cls, user):
    cursor.execute("SELECT impresoras.id, modelo, tipo_color, wifi, escaner, precio, observaciones, link1, link2, calificaciones.id, calificaciones.user_id, calificaciones.impresora_id, calificaciones.calificacion, calificaciones.created_at, calificaciones.updated_at FROM impresoras JOIN calificaciones ON calificaciones.impresora_id = impresoras.id AND calificaciones.user_id = %s ORDER BY calificaciones.updated_at DESC LIMIT 10", (user.id,))
    return [cls(*record) for record in cursor.fetchall()]