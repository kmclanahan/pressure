import psycopg2

conn = psycopg2.connect(database="travel_info", user="postgres", password="pass1234", host="localhost", port="5432")
cur = conn.cursor()


cur.execute("DELETE FROM Twitter_Data WHERE threat_type = 'Fake'")

conn.commit()
conn.close()

