
from nltk.tokenize import word_tokenize
tweet = "Martin Luther King, Jr's Most Tweeted Quotes in 2013#twitter"
print(word_tokenize(tweet))


import re
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

def tokenize(s):
    return tokens_re.findall(s)

def preprocess(s, lowercase=False):
    tokens = tokenize(s)
    if lowercase:
        tokens = [token if emoticon.re.search(token) else token.lower() for token in tokens]
    return tokens


import pandas as pd
with open('tweets.csv', 'r') as f:
    for line in f:
        tweet = pd.loads(line)
        tokens = preprocess(tweet['text'])
            

import operator
from collections import Counter
import pandas as pd

fname = 'tweets.csv'
with open(fname, 'r') as f:
    count_all = Counter()
    for line in f:
        tweet = pd.loads(line)
        #create a list with all the terms
        terms_all = [term for term in preprocess(tweet['text'])]
        #update the counter
        count_all.update(terms_all)
    #print the first 20 most frequent words
    print(count_all.most_common(20))


from nltk.corpus import stopwords
import string

punctuation = list(string.punctuation)
stop = stopwords.words('english') + punctuation + ['rt','via']

terms_stop = [term for term in preprocess(tweet['text']) if term not in stop]


#count terms only once
count_single = set(terms_all)
#count hashtags
count_hashtags = [term for term in preprocess(tweet['text'])
                 if term.startswith('#')]
#count terms only
terms_only = [term for term in preprocess(tweet['text'])
             if term not in stop and
             not term.startswith(('#','@'))]


from nltk import bigrams
terms_bigrams = bigrams(terms_stop)
