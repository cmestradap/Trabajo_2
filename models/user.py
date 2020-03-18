import psycopg2
from database import cursor, connection
from passlib.context import CryptContext

class User:
  __pwd_context = CryptContext(
    schemes = ["pbkdf2_sha256"],
    default = "pbkdf2_sha256",
    pbkdf2_sha256__default_rounds = 30000
  )

  def __init__(self, id, name, email, password):
    self.id = id
    self.name = name
    self.email = email
    self.__password = password

  @classmethod
  def create(cls, name, email, password):
    encrypted = cls.__pwd_context.encrypt(password)
    return cls(None, name, email, encrypted)

  @classmethod
  def find(cls, email):
    try:
      cursor.execute("SELECT id, name, email, password FROM users WHERE email = %s", (email,))
      record = cursor.fetchone()
      if record:
        return cls(*record)
      else:
        return None

    except (Exception, psycopg2.Error) as error:
      print ("Error while connecting to PostgreSQL:", error)
      return None

  def insert(self):
    try:
      cursor.execute("INSERT INTO users (name, email, password) VALUES(%s, %s, %s)", (self.name, self.email, self.__password))
      connection.commit()
      return True
    except (Exception, psycopg2.Error) as error:
      connection.rollback()
      print ("Error while connecting to PostgreSQL", error)
      return False

  def verify(self, input_password):
    return User.__pwd_context.verify(input_password, self.__password)