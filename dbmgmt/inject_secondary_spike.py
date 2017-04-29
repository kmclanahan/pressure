import psycopg2

conn = psycopg2.connect(database="travel_info", user="postgres", password="pass1234", host="localhost", port="5432")
cur = conn.cursor()

cur.execute("Truncate Tweet_Spike_Data")
cur.execute("Truncate Tweet_Spike_Text")

tweets = [ "30 killed in gombe bombing",
           "senseless violence",
           "gombe is in a state of emergency",
           "I hope everyone is ok at the bus station",
           "innocent people killed today in gombe bombing",
           "#terrorism is the dumbest thing humans do",
           "deadly bomb blasts bust station in #Gombe",
           "bombing at #gombe terminal bus station",
           "smoke is everywhere, I hope everyone is safe",
           "that was definitely a bomb #gombe",
           "loud explosion near my house",
           "big bomb just went off in #gombe",
           "praying for #gombe",
           "what the hell just happened in gombe?" ]

fixed_spike_words = "bomb dead emergency explosion gombe station"
fixed_spike_hashes = "#gombe #terrorism"

cur.execute("INSERT INTO Tweet_Spike_Data (idx, ts, grid_idx, baseline_level, current_level, spike_percent, top_words, top_hashes, latitude, longitude) VALUES ( 1, now(), '(32,32)', 25.5, 612, 2400, '%s', '%s', 10.286707, 11.165499)" %(fixed_spike_words, fixed_spike_hashes))

for tweet in tweets:
    cur.execute("INSERT INTO Tweet_Spike_Text (ts, spike_idx, tweet, latitude, longitude) VALUES ( now(), 1, '%s', 10.287, 11.169)" %tweet)


conn.commit()
conn.close()

print "Spike injected in Gombe, Nigeria"
