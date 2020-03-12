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
    user = "fwlnuygvpzvpis",
    password = "da023af44eb4d87c3587ddd2edb09d2a43263dbb4405a86ec99dc34d05baaad8",
    host = "ec2-54-197-48-79.compute-1.amazonaws.com",
    port = "5432",
    database = "d54hmasrunnmlg"
  )
  cursor = connection.cursor()
  cursor.execute("SELECT version();")
  record = cursor.fetchone()
  print("You are connected to - ", record, "\n")

except (Exception, psycopg2.Error) as error:
  print ("Error while connecting to PostgreSQL", error)
  exit()