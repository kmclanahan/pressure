import psycopg2, datetime

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

#initialze the grid with empty arrays
tweet_grid = {}

for i in range(lat_grid):
    for j in range(long_grid):
        count_array_24h = [None] * 24

        for t in range(len(count_array_24h)):
            count_array_24h[t] = []

        tweet_grid[(i,j)] = count_array_24h


#connect to the database and calculate the tweet counts per square per hour
conn = psycopg2.connect(database="travel_info", user="postgres", password="pass1234", host="localhost", port="5432")
cur = conn.cursor()

end_time = datetime.datetime.now()

#d1 = datetime.date(2017, 3, 10)
#t1 = datetime.time(0, 0, 0)
delta = datetime.timedelta(hours=1)
start_delta = datetime.timedelta(days=7)

start_time = end_time - start_delta - delta
hour = 0

while start_time < end_time:

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

    print "finished processing hour %s" %hour
    start_time += delta
    hour += 1

for idx in tweet_grid:
    print idx
    print tweet_grid[idx]
