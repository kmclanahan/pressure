
import psycopg2


conn = psycopg2.connect(user="postgres", password="pass1234", host="localhost", port="5432")
cur = conn.cursor()
cur.connection.set_isolation_level(0)

conn = psycopg2.connect(dbname="travel_info", user="postgres", password="pass1234", host="localhost", port="5432")
cur = conn.cursor()

cur.execute("CREATE TABLE Profile(ID SERIAL PRIMARY KEY, name varchar, email varchar, phone varchar, contact_name varchar, contact_email varchar, contact_phone varchar)")


cur.close()

conn.commit()
conn.close()

print "created table Profile"
