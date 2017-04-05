import psycopg2

conn = psycopg2.connect(database="travel_info", user="postgres", password="pass1234", host="localhost", port="5432")
cur = conn.cursor()

cur.execute("SELECT * FROM Tweet_Spike_Data")

all_data = cur.fetchall()

print "Spike information:"
for data in all_data:
    print data

print "-----------------"
print "Tweet Data:"

cur.execute("SELECT * FROM Tweet_Spike_Text")

all_data = cur.fetchall()

for data in all_data:
    print data

conn.commit()
conn.close()

