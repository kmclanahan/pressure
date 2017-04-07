import psycopg2, datetime, time
from nltk.tokenize import word_tokenize
import re, operator, string
from collections import Counter
from nltk.corpus import stopwords

######### CONSTANTS #######

DEBUG = True

start_lat = -37.0
start_long = -21.74
end_lat = 36.89
end_long = 54.55
dist_lat = end_lat - start_lat
dist_long = end_long - start_long

#change these to modify the resolution of the grid
lat_grid = 20
long_grid = 20

#how many days of history to track
day_hist = 7

lat_grid_len = dist_lat/lat_grid
long_grid_len = dist_long/long_grid

tweet_percent_threshold = 200
min_term_length = 3
####### HELPER FUNCTIONS #######

#calculates lat/long from the coordinates of the tweet
def get_lat_long(coords):
    c_list = coords.split(',')
    
    if len(c_list) != 8:
        print "Error calculating lat,long"
        return -1            
    
    longitude = 0.25*(float(c_list[0].strip("{}")) +
                      float(c_list[2].strip("{}")) +
                      float(c_list[4].strip("{}")) +
                      float(c_list[6].strip("{}")))
                
    latitude = 0.25*(float(c_list[1].strip("{}")) +
                      float(c_list[3].strip("{}")) +
                      float(c_list[5].strip("{}")) +
                      float(c_list[7].strip("{}")))

    if latitude < start_lat or latitude > end_lat or longitude < start_long or longitude > end_long:
        return -1

    return (latitude, longitude)

#calculates a grid index for a given lat/long
def get_grid_index(lat_long_tup):

    latitude = lat_long_tup[0]
    longitude = lat_long_tup[1]

    lat_offset = latitude - start_lat
    long_offset = longitude - start_long
    
    lat_idx = int(lat_offset/lat_grid_len)
    long_idx = int(long_offset/long_grid_len)

    if lat_idx >= lat_grid or long_idx >= long_grid:
        print "idx out of range (%s, %s)" %(lat_idx, long_idx)
        return -1

    return( (lat_idx, long_idx) )

def get_lat_long_from_sector(idx):
    lower_lat = start_lat + lat_grid_len*idx[0]
    upper_lat = start_lat + lat_grid_len*(idx[0]+1)
    lower_long = start_long + long_grid_len*idx[1]
    upper_long = start_long + long_grid_len*(idx[1]+1)
    return [lower_lat, lower_long, upper_lat, upper_long]

def update_grid(start_time):
    delta_time = start_time + delta

    cur.execute("SELECT coordinates FROM Twitter_Data WHERE ts > '%s' and ts < '%s'" %(start_time, delta_time))

    all_data = cur.fetchall()

    #initialize the temp grid for this hour
    temp_grid = {}
    for i in range(lat_grid):
        for j in range(long_grid):
            temp_grid[(i,j)] = 0

    for data in all_data:
        lat_long_tup = get_lat_long( data[0] )
        if lat_long_tup != -1:
            idx = get_grid_index( lat_long_tup )
            if idx != -1:
                temp_grid[idx] += 1

    #add all the counts for this hour into the tweet_grid
    for idx in temp_grid:
        #keep a 7-day history of each hour
        if len(tweet_grid[idx][hour % 24]) >= day_hist:
            tweet_grid[idx][hour % 24] = tweet_grid[idx][hour % 24][1:]
        tweet_grid[idx][hour % 24].append(temp_grid[idx])

emoticons_str = r"""
    (?:
        [:=;] #eyes
        [oO\-] #nose
        [D\)\]\(\]/\\OpP] #mouth
    )"""


regex_str = [
    emoticons_str,
    r'<[^>]+>', # HTML tags
    r'(?:@[\w_]+)', # @-mentions
    r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", # hash-tags
    r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', # URLs

    r'(?:(?:\d+,?)+(?:\.?\d+)?)', # numbers
    r"(?:[a-z][a-z'\-_]+[a-z])", # words with - and '
    r'(?:[\w_]+)', # other words
    r'(?:\S)' # anything else
]

tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)
emoticon_re = re.compile(r'^'+emoticons_str+'$', re.VERBOSE | re.IGNORECASE)
punctuation = list(string.punctuation)
stop = stopwords.words('english') + punctuation + ['rt','via']

def tokenize(s):
    return tokens_re.findall(s)

def preprocess(s, lowercase=False):
    tokens = tokenize(s)
    if lowercase:
        tokens = [token if emoticon.re.search(token) else token.lower() for token in tokens]
    return tokens

def get_most_common_words(tweet_list, num):
    count_all = Counter()
    for tweet in tweet_list:
        #create a list with all the terms
        terms_all = [term for term in preprocess(tweet[0]) if term not in stop
                     and not term.startswith(('#', '@', 'http'))
                     and len(term) > min_term_length]
        #update the counter
        count_all.update(terms_all)
    #print the first 20 most frequent words
    return ' '.join(str(e[0]) for e in count_all.most_common(num))

def get_most_common_hashtags(tweet_list, num):
    count_all = Counter()
    for tweet in tweet_list:
        #create a list with all the terms
        terms_all = [term for term in preprocess(tweet[0]) if term.startswith('#') and len(term) > min_term_length]
        #update the counter
        count_all.update(terms_all)
    #print the first 20 most frequent words
    return ' '.join(str(e[0]) for e in count_all.most_common(num))

####### MONITORING APPLICATION #######

#initialze the grid with empty arrays
tweet_grid = {}

for i in range(lat_grid):
    for j in range(long_grid):
        count_array_24h = [None] * 24

        for t in range(len(count_array_24h)):
            count_array_24h[t] = []

        tweet_grid[(i,j)] = count_array_24h

tweet_grid_averages = {}

def update_grid_averages():
    for idx in tweet_grid:
        tweet_grid_averages[idx] = []
        for values in tweet_grid[idx]:
            avg_values = filter(lambda x: x!= 0, values)
            if len(avg_values) != 0:
                tweet_grid_averages[idx].append(sum(avg_values)/float(len(avg_values)))
            else:
                tweet_grid_averages[idx].append(0)

#connect to the database and calculate the tweet counts per square per hour
conn = psycopg2.connect(database="travel_info", user="postgres", password="pass1234", host="localhost", port="5432")
cur = conn.cursor()

end_time = datetime.datetime.now()

#d1 = datetime.date(2017, 3, 10)
#t1 = datetime.time(0, 0, 0)
delta = datetime.timedelta(hours=1)
start_delta = datetime.timedelta(days=7)

start_time = end_time - start_delta - delta
first_time = start_time

hour = 0

print "Processing 7 days worth of history... Please Wait..."

while start_time < end_time:

    update_grid(start_time)

    start_time += delta
    hour += 1

    if hour % 24 == 0:
        print "Finished processing day %s..." %(hour / 24)

update_grid_averages()

if (DEBUG):
    for i in range(lat_grid):
        for j in range(long_grid):
            idx = (i,j)
            print "---(%s,%s)---" %idx
            print "---tweet_grid---"
            print tweet_grid[idx]
            print "----averages----"
            print tweet_grid_averages[idx]

#emter monitoring loop
loop_freq_mins = 1
loop_count = 0

conn.commit()
conn.close()

#function to get the correct hour index from a timestamp
def get_hour_idx(ts):
    seconds_in_hour = 60 * 60
    diff = ts - first_time

    return int(diff.seconds / seconds_in_hour)

while True:
    print "Entering loop %s..." %loop_count
    current_time = datetime.datetime.now()

    time_diff = current_time - start_time

    #now check to see if any counts are abnormally high
    conn = psycopg2.connect(database="travel_info", user="postgres", password="pass1234", host="localhost", port="5432")
    cur = conn.cursor()

    #clean up old tweet spike data
    cur.execute("Truncate Tweet_Spike_Data")
    cur.execute("Truncate Tweet_Spike_Text")


    #if an hour has passed, update the grid
    if time_diff.seconds > (60 * 60):
        print "Updating grid history..."
        update_grid(start_time)
        update_grid_averages()
        start_time += delta  

    one_hour_ago = current_time - delta

    cur.execute("SELECT coordinates FROM Twitter_Data WHERE ts > '%s' and ts < '%s'" %(one_hour_ago, current_time))

    all_data = cur.fetchall()

    #initialize the temp grid for this hour
    temp_grid = {}
    for i in range(lat_grid):
        for j in range(long_grid):
            temp_grid[(i,j)] = 0

    for data in all_data:
        lat_long_tup = get_lat_long( data[0] )
        if lat_long_tup != -1:
            idx = get_grid_index( lat_long_tup )
            if idx != -1:
                temp_grid[idx] += 1

    #get the right hour index into the grid
    hour_idx = get_hour_idx(current_time)

    spike_idx = 1
    for idx in tweet_grid_averages:
        baseline = tweet_grid_averages[idx][hour_idx] + 1
        observed = temp_grid[idx] + 1

        percent_increase = 100.0*(observed - baseline)/baseline

        if observed - baseline < 10:
            continue

        if percent_increase > tweet_percent_threshold:
            print ">%s%% increase for sector (%s,%s): observed %s, baseline %s" %(tweet_percent_threshold, idx[0], idx[1], observed, baseline)
            boundaries = get_lat_long_from_sector(idx)

            cur.execute("SELECT tweet, ts, latitude, longitude FROM Twitter_Data WHERE latitude > '%s' and latitude < '%s' and longitude > '%s' and longitude < '%s' and ts > '%s' and ts < '%s'" %(boundaries[0], boundaries[2], boundaries[1], boundaries[3], one_hour_ago, current_time))

            all_data = cur.fetchall()

            print "Top 10 words:"
            top_words = get_most_common_words(all_data, 10)
            print top_words
            print "Top 10 hashtags:"
            top_hashes = get_most_common_hashtags(all_data, 10)
            print top_hashes

            num_tweets, sum_lat, sum_long = 0,0,0
            #add the tweet text 
            for data in all_data:
                tweet, ts, latitude, longitude = data
                cur.execute("INSERT INTO Tweet_Spike_Text (ts, spike_idx, tweet, latitude, longitude) VALUES ( %s, %s, %s, %s, %s)", (ts, spike_idx, tweet, latitude, longitude))
                sum_lat += latitude
                sum_long += longitude
                num_tweets += 1

            #calculate the average lat/long for the tweet spike
            latitude = sum_lat / num_tweets
            longitude = sum_long / num_tweets 

            #add the data to the spike table
            cur.execute("INSERT INTO Tweet_Spike_Data (idx, ts, grid_idx, baseline_level, current_level, spike_percent, top_words, top_hashes, latitude, longitude) VALUES ( %s, now(), %s, %s, %s, %s, %s, %s, %s, %s)", (spike_idx, idx, baseline, observed, percent_increase, top_words, top_hashes, latitude, longitude))

            spike_idx += 1
 


    conn.commit()
    conn.close()
    loop_count += 1
    time.sleep(loop_freq_mins * 60)


