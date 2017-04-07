import psycopg2

fake_data = ["Trump", "Trump blows", "Trump blows goats", "Trump blows goats", "Trump blows goats",
               "Trump blows goats", "Trump blows goats", "Trump blows goats", "Trump blows goats",
               "Trump blows goats", "Trump blows goats", "Trump blows goats", "Trump blows goats",
               "Trump blows goats", "Trump blows goats", "Trump blows goats", "Trump blows goats",
               "Trump blows goats", "Trump blows goats", "Trump blows goats", "Trump blows goats",
               "Trump blows goats", "Trump blows goats", "Trump blows goats", "Trump blows goats",
               "Trump blows goats #fakenews", "Trump blows goats #fakenews", "Trump blows goats #fakenews",
               "Trump blows goats #fakenews", "Trump blows goats #fakenews", "Trump blows goats #fakenews",
               "Trump blows goats #fakenews", "Trump blows goats #fakenews", "Trump blows goats #fakenews",
              ]

longitude = 33.754758
latitude = -13.994795
#coords = [[-13.994795, 33.754758], [-13.994795, 33.754758], [-13.994795, 33.754758], [-13.994795, 33.754758]]
coords = [[33.754758, -13.994795], [33.754758, -13.994795], [33.754758, -13.994795], [33.754758, -13.994795]]

conn = psycopg2.connect(database="travel_info", user="postgres", password="pass1234", host="localhost", port="5432")
cur = conn.cursor()


for fd in fake_data:
    cur.execute("INSERT INTO Twitter_Data (ts, tweet, location, country, language, coordinates, threat_type, latitude, longitude) VALUES ( now(), %s, %s, %s, %s, %s, %s, %s, %s)", (fd, 'Lilongwe', 'Malawi', 'en', coords, 'Fake', latitude, longitude))

conn.commit()
conn.close()

print "Spike injected in Malawi"
