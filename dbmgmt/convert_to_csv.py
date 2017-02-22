import psycopg2
import sys, re

filename = sys.argv[1].strip()

num_records = "ALL"

if len(sys.argv) > 2:
    num_records = sys.argv[2].strip()

print "Writing database to %s" %filename

conn = psycopg2.connect(database="travel_info", user="postgres", password="pass1234", host="localhost", port="5432")
cur = conn.cursor()

query = "SELECT * FROM Twitter_Data LIMIT %s" %num_records

cur.execute(query)

count = 0
all_data = cur.fetchall()

with open(filename, 'w') as outfile:
    for data in all_data:

        dbid, tweet, loc_name, country, language, coords, ttype = data

        tweet = re.sub('\n', '', tweet)

        c_list = coords.split(',')
    
        if len(c_list) != 8:
            print "Error calculating lat,long"
            break            
    
        longitude = 0.25*(float(c_list[0].strip("{}")) +
                      float(c_list[2].strip("{}")) +
                      float(c_list[4].strip("{}")) +
                      float(c_list[6].strip("{}")))
                
        lattitude = 0.25*(float(c_list[1].strip("{}")) +
                      float(c_list[3].strip("{}")) +
                      float(c_list[5].strip("{}")) +
                      float(c_list[7].strip("{}")))

        outfile.write('%s,%s,%s,%s,"""%s"""\n' 
                    %(dbid, language, lattitude, longitude, tweet) )

        count += 1

conn.commit()
conn.close()

print "\nWrote %s Tweets to %s" %(count, filename)
