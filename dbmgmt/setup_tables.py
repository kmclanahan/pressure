
import psycopg2


conn = psycopg2.connect(user="postgres", password="pass1234", host="localhost", port="5432")
cur = conn.cursor()
cur.connection.set_isolation_level(0)

conn = psycopg2.connect(dbname="travel_info", user="postgres", password="pass1234", host="localhost", port="5432")
cur = conn.cursor()

try:
    cur.execute("DROP TABLE Tweet_Spike_Data")
    cur.execute("DROP TABLE Tweet_Spike_Text")
except:
    pass

cur.execute("CREATE TABLE Tweet_Spike_Data(idx integer, ts timestamp, grid_idx varchar, spike_percent float, top_words varchar, top_hashes varchar, latitude float, longitude float)")

cur.execute("CREATE TABLE Tweet_Spike_Text(id serial PRIMARY KEY, ts timestamp, spike_idx integer, tweet varchar, latitude float, longitude float)")

cur.close()

conn.commit()
conn.close()

print "created table Tweet_Spike_Data"
print "created table Tweet_Spike_Text"

