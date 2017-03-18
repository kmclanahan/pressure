from __future__ import absolute_import, print_function, unicode_literals

from collections import Counter
from streamparse.bolt import Bolt
import string
import psycopg2

def ascii_string(s):
  return all(ord(c) < 128 for c in s)

class WordCounter(Bolt):

    outputs = ['name', 'counts', 'tweet', 'country', 'language', 'coords']

    def initialize(self, conf, ctx):
        self.counts = Counter()
        # self.redis = StrictRedis()

    def process(self, tup):
        tweet = tup.values[0]
        location = tup.values[1]
        country = tup.values[2]
        language = tup.values[3]
        coords = tup.values[4][0]

        longitude = 0.25*(float(coords[0][0]) +
                          float(coords[1][0]) +
                          float(coords[2][0]) +
                          float(coords[3][0]) )


        latitude = 0.25*(float(coords[0][1]) +
                         float(coords[1][1]) +
                         float(coords[2][1]) +
                         float(coords[3][1]) )
 
        printable = set(string.printable)
        tweet = filter(lambda x: x in printable, tweet)
        location = filter(lambda x: x in printable, location)
        # Write codes to increment the word count in Postgres
        # Use psycopg to interact with Postgres
        # Database name: Tcount 
        # Table name: Tweetwordcount 
        # you need to create both the database and the table in advance.

        try:
            conn = psycopg2.connect(database="travel_info", user="postgres", password="pass1234", host="localhost", port="5432")

            cur = conn.cursor()

            cur.execute("INSERT INTO Twitter_Data (ts, tweet, location, country, language, coordinates, threat_type, latitude, longitude) VALUES ( now(), %s, %s, %s, %s, %s, %s, %s, %s)", (tweet, location, country, language, coords, 'None', latitude, longitude))

            conn.commit()
            conn.close()

            self.counts['Tweets'] += 1
            self.emit([location, self.counts['Tweets'], tweet, country, language, coords])
        except:
            self.log("Cannot log tweet... %s" % tweet)

        # Log the count - just to see the topology running
        try:
            self.log('%s: %d %s %s' % (location, self.counts['Tweets'], country, coords))
            self.log(tweet)
        except:
            pass
