import psycopg2
import subprocess
import time

conn = psycopg2.connect(database="travel_info", user="postgres", password="pass1234", host="localhost", port="5432")
cur = conn.cursor()

cur.execute("SELECT id FROM Twitter_Data")

all_data = cur.fetchall()

prev_count = len(all_data)

time_interval_mins = 5

while True:
    cur.execute("SELECT id FROM Twitter_Data")

    all_data = cur.fetchall()

    count = len(all_data)

    print "Found %s records" %count

    if count == prev_count:
        print "Count did not increase, restarting app..."
        subprocess.Popen(["sparse", "run"])

    prev_count = count
    time.sleep(time_interval_mins * 60)
