# This script will drop all the data in the travel_info table and recreate the database
# DO NOT RUN THIS UNLESS YOU WANT TO LOSE ALL THE DATA!!!

import psycopg2


conn = psycopg2.connect(user="postgres", password="pass1234", host="localhost", port="5432")
cur = conn.cursor()
cur.connection.set_isolation_level(0)

try:
    cur.execute("CREATE DATABASE travel_info")
except:
    cur.execute("DROP DATABASE travel_info")
    cur.execute("CREATE DATABASE travel_info")

conn.commit()
conn.close()

conn = psycopg2.connect(dbname="travel_info", user="postgres", password="pass1234", host="localhost", port="5432")
cur = conn.cursor()
cur.connection.set_isolation_level(0)
cur.execute("CREATE TABLE Twitter_Data(id serial PRIMARY KEY, ts timestamp, tweet varchar, location varchar, country varchar, language varchar, coordinates varchar, threat_type varchar, longitude float, latitude float)")

cur.close()

conn.commit()
conn.close()

print "created database travel_info"
print "created table Twitter_Data"

