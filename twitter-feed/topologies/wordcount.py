"""
Word count topology
"""

from streamparse import Grouping, Topology

from bolts.wordcount import WordCounter
from spouts.tweets import Tweets 


class WordCount(Topology):
    tweet_spout = Tweets.spec()
    count_bolt = WordCounter.spec(inputs={tweet_spout: Grouping.fields('tweet')}, par=55555)
