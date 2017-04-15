
import psycopg2


conn = psycopg2.connect(user="postgres", password="pass1234", host="localhost", port="5432")
cur = conn.cursor()
cur.connection.set_isolation_level(0)

conn = psycopg2.connect(dbname="travel_info", user="postgres", password="pass1234", host="localhost", port="5432")
cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS Tweet_Spike_Data")
cur.execute("DROP TABLE IF EXISTS Tweet_Spike_Text")
cur.execute("DROP TABLE IF EXISTS Tweet_Spike_History")
cur.execute("DROP TABLE IF EXISTS Tweet_Spike_Text_History")

cur.execute("CREATE TABLE Tweet_Spike_Data(idx integer, ts timestamp, grid_idx varchar, baseline_level float, current_level float, spike_percent float, top_words varchar, top_hashes varchar, latitude float, longitude float)")

cur.execute("CREATE TABLE Tweet_Spike_Text(id serial PRIMARY KEY, ts timestamp, spike_idx integer, tweet varchar, latitude float, longitude float)")

cur.execute("CREATE TABLE Tweet_Spike_History(id serial PRIMARY KEY, ts timestamp, grid_idx varchar, baseline_level float, current_level float, spike_percent float, top_words varchar, top_hashes varchar, latitude float, longitude float, relevant integer DEFAULT 2)")

cur.execute("CREATE TABLE Tweet_Spike_Text_History(id serial PRIMARY KEY, ts timestamp, spike_idx integer, tweet varchar, latitude float, longitude float)")

cur.close()

conn.commit()
conn.close()

print "created table Tweet_Spike_Data"
print "created table Tweet_Spike_Text"
print "created table Tweet_Spike_History"
print "created table Tweet_Spike_Text_History"

