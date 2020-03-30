import psycopg2
import atexit

def close_database():
  if connection:
    cursor.close()
    connection.close()
    print("Database connection is closed")

atexit.register(close_database)

try:
  connection = psycopg2.connect(
    user = "enfygpfuflrodx",
    password = "76b10139db87c5edc4a53ecbdfc07731579217b5a049e194b81556c4143bdd61",
    host = "ec2-50-17-21-170.compute-1.amazonaws.com",
    port = "5432",
    database = "dac8g4tkukt2e4"
  )
  cursor = connection.cursor()
  cursor.execute("SELECT version();")
  record = cursor.fetchone()
  print("You are connected to - ", record, "\n")

except (Exception, psycopg2.Error) as error:
  print ("Error while connecting to PostgreSQL", error)
  exit()