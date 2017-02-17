import psycopg2

conn = psycopg2.connect(database="travel_info", user="postgres", password="pass1234", host="localhost", port="5432")
cur = conn.cursor()

cur.execute("SELECT country, language FROM Twitter_Data")

countries = {}
languages = {}
count = 0
all_data = cur.fetchall()

for data in all_data:
    countries.setdefault(data[0], 0)
    countries[data[0]] += 1

    languages.setdefault(data[1], 0)
    languages[data[1]] += 1

    count += 1

conn.commit()
conn.close()

for country in countries:
    print "%s:\t%s" %(country, countries[country])

for language in languages:
    print "%s\t%s" %(language, languages[language])

print("\nTotal Tweets Logged: %s" %count)
