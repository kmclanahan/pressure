import psycopg2, datetime, time

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

    #if an hour has passed, update the grid
    if time_diff.seconds > (60 * 60):
        print "Updating grid history..."
        update_grid(start_time)
        update_grid_averages()
        start_time += delta

    #now check to see if any counts are abnormally high
    conn = psycopg2.connect(database="travel_info", user="postgres", password="pass1234", host="localhost", port="5432")
    cur = conn.cursor()

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

    for idx in tweet_grid_averages:
        baseline = tweet_grid_averages[idx][hour_idx] + 1
        observed = temp_grid[idx] + 1

        percent_increase = 100.0*(observed - baseline)/baseline

        if observed - baseline < 10:
            continue

        if percent_increase > 300:
            print ">300%% increase for sector (%s,%s): observed %s, baseline %s" %(idx[0], idx[1], observed, baseline)
        elif percent_increase > 200:
            print ">200%% increase for sector (%s,%s): observed %s, baseline %s" %(idx[0], idx[1], observed, baseline)
        elif percent_increase > 100:
            print ">100%% increase for sector (%s,%s): observed %s, baseline %s" %(idx[0], idx[1], observed, baseline)
        elif percent_increase > 50:
            print ">50%% increase for sector (%s,%s): observed %s, baseline %s" %(idx[0], idx[1], observed, baseline)

    conn.commit()
    conn.close()
    loop_count += 1
    time.sleep(loop_freq_mins * 60)


