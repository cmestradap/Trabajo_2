import psycopg2
import datetime
from database import cursor, connection

class Rating:
  def __init__(self, id, user_id, printer_id, rating, created_at, updated_at):
    self.id = id
    self.user_id = user_id
    self.printer_id = printer_id
    self.rating = rating if rating else 0.0
    self.created_at = created_at
    self.updated_at = updated_at

  def empty(self):
    return self.id == None

  def rate(self, q, user):
    if self.rating == q: 
      return False

    dt = datetime.datetime.now()
    try:
      if self.id:
        cursor.execute("UPDATE calificaciones SET calificacion = %s, updated_at = %s WHERE id = %s", (q, dt, self.id))
        connection.commit()
      else:
        cursor.execute("INSERT INTO calificaciones (user_id, impresora_id, calificacion, created_at, updated_at) VALUES(%s, %s, %s, %s, %s) RETURNING id", (user.id, self.printer_id, q, dt, dt))
        connection.commit()
        self.id = cursor.fetchone()[0]  
      return True

    except (Exception, psycopg2.Error) as error:
      connection.rollback()
      print ("Error while connecting to PostgreSQL", error)
      return False

  @classmethod
  def has_ratings(cls, user):
    cursor.execute("SELECT EXISTS(SELECT id FROM calificaciones WHERE calificaciones.user_id = %s)", (user.id,))
    return cursor.fetchone()[0]