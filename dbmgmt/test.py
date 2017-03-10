import psycopg2

conn = psycopg2.connect(database="travel_info", user="postgres", password="pass1234", host="localhost", port="5432")

cur = conn.cursor()

cur.execute("INSERT INTO Twitter_Data (ts, tweet, location, country, language, coordinates, threat_type) VALUES ( now(), tweet, location, country, language, [40,32], 0))

conn.commit()
conn.close()
