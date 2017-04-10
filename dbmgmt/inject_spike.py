import psycopg2

fake_data_0 = ["Bomb", "Bomb explosion"]
fake_data_1 = ["bomb explosion serowe"]
fake_data_2 = ["bomb explosion serowe #fakenews"]

fake_data = fake_data_0 + fake_data_1*300 + fake_data_2*150

longitude = 26.430279
latitude = -22.495676
#coords = [[-13.994795, 33.754758], [-13.994795, 33.754758], [-13.994795, 33.754758], [-13.994795, 33.754758]]
coords = [[longitude, latitude], [longitude, latitude], [longitude, latitude], [longitude, latitude]]

conn = psycopg2.connect(database="travel_info", user="postgres", password="pass1234", host="localhost", port="5432")
cur = conn.cursor()


for fd in fake_data:
    cur.execute("INSERT INTO Twitter_Data (ts, tweet, location, country, language, coordinates, threat_type, latitude, longitude) VALUES ( now(), %s, %s, %s, %s, %s, %s, %s, %s)", (fd, 'Thbala', 'Botswana', 'en', coords, 'Fake', latitude, longitude))

conn.commit()
conn.close()

print "Spike injected in Botswana"
