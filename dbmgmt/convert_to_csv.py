import psycopg2
import sys

filename = sys.argv[1].strip()

print "Writing database to %s" %filename

conn = psycopg2.connect(database="travel_info", user="postgres", password="pass1234", host="localhost", port="5432")
cur = conn.cursor()

query = "SELECT * FROM Twitter_Data"

cur.execute(query)

count = 0
all_data = cur.fetchall()

with open(filename, 'w') as outfile:
    for data in all_data:

        outfile.write('"""%s""","""%s""","""%s""","""%s""","""%s""","""%s""","""%s"""\n' 
                    %(data[0], data[1], data[2], data[3], data[4], data[5], data[6]) )

        count += 1

conn.commit()
conn.close()

print "\nWrote %s Tweets to %s" %(count, filename)
