import psycopg2

conn = psycopg2.connect(database="travel_info", user="postgres", password="pass1234", host="localhost", port="5432")
cur = conn.cursor()

cur.execute("SELECT * FROM Tweet_Spike_History")

all_data = cur.fetchall()

print "Spike information:"
print "------------------"
for data in all_data:
    print data
    
    cur.execute("SELECT * FROM Tweet_Spike_Text_History WHERE spike_idx = %s" %(data[0]) )

    print "Tweets:"
    print "------------------"
    tweet_data = cur.fetchall()
    for td in tweet_data:
        print td

    print "------------------"

conn.commit()
conn.close()

