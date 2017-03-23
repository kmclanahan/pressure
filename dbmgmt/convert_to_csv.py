import psycopg2
import sys, re

filename = sys.argv[1].strip()

num_records = "ALL"

if len(sys.argv) > 2:
    num_records = sys.argv[2].strip()

print "Writing database to %s" %filename

conn = psycopg2.connect(database="travel_info", user="postgres", password="pass1234", host="localhost", port="5432")
cur = conn.cursor()

query = "SELECT * FROM Twitter_Data LIMIT %s" %num_records

cur.execute(query)

count = 0
all_data = cur.fetchall()

with open(filename, 'w') as outfile:
    for data in all_data:

        dbid, ts, tweet, loc_name, country, language, coords, ttype, longitude, latitude = data

        tweet = re.sub('\n', '', tweet)
        tweet = re.sub('"', '', tweet)

        outfile.write('%s,%s,%s,%s,%s,"%s"\n' 
                    %(dbid, ts, language, latitude, longitude, tweet) )

        count += 1

conn.commit()
conn.close()

print "\nWrote %s Tweets to %s" %(count, filename)
