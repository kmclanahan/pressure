import psycopg2
import sys

keyword = sys.argv[1].strip()

print "Searching database for %s" %keyword

conn = psycopg2.connect(database="travel_info", user="postgres", password="pass1234", host="localhost", port="5432")
cur = conn.cursor()

query = "SELECT country, tweet FROM Twitter_Data WHERE tweet LIKE '%%%s%%'" %keyword

print query

cur.execute(query)

countries = {}
count = 0
all_data = cur.fetchall()

for data in all_data:
    countries.setdefault(data[0], 0)
    countries[data[0]] += 1

    print "%s:\t%s" %(data[0], data[1])

    count += 1

conn.commit()
conn.close()

for country in countries:
    print "%s:\t%s" %(country, countries[country])

print "\nTotal Tweets containing %s: %s" %(keyword, count)
