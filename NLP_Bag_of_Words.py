
# coding: utf-8

#capstone - bag of words using tweets

from collections import Counter
import pandas as pd

#Type in some sample tweets from BigQuery
tweets = ["Two earthquakes hit Ecuador today and now a plane from Paris is missing??",
         "Gotta come on Twitter to make sure that was an earthquake and I'm not tripping",
         "BREAKING: Nepal earthquake toll exceeds 1100 and is expected to rise",
         "	@Teresa_Giudice Prayers 4 u and extended family in Italy in wake of 6.2 earthquake",
         "Bruh was that an earthquake? I swear my bed was hella rockin and I'm laying still!"]


#find all the unique words in the tweets
unique_words = list(set(" ".join(tweets).split(" ")))
def make_matrix(tweets, vocab):
    matrix = []
    for tweet in tweets:
        #count each word first and then make a matrix
        counter = Counter(tweet)
        row = [counter.get(w,0) for w in vocab]
        matrix.append(row)
    df = pd.DataFrame(matrix)
    df.columns = unique_words
    return df

#print out the matrix
print(make_matrix(tweets, unique_words))

import re
#convert to lowercase, then replace any non-letter, space or digit character in the tweets
new_tweets = [re.sub(r'[^\w\s\d]', '',t.lower()) for t in tweets]

#replace sequences of whitespace with a space character
new_tweets = [re.sub("\s+", " ", t) for t in new_tweets]

unique_words = list(set(" ". join(new_tweets).split(" ")))
print(make_matrix(new_tweets, unique_words))


##this slowed down and eventually crashed my notebook##
#import nltk
#nltk.download('all')


#removing stopwords
with open("stop_words.txt", "r") as f:
    stopwords = f.read().split("\n")

#I tried to get the nltk stopwords which crashed my system
#from nltk.corpus import stopwords
#print(stopwords.words("english"))

#words = [w for w in words if not w in stopwords.words("english")]
#print(words)

#remove punctuatuon again
words = [re.sub(r'[^\w\s\d]','',s.lower()) for s in words]

unique_words = list(set(" ".join(new_tweets).split(" ")))

#remove stopwords from vocabulary
unique_words = [w for w in unique_words if w not in words]

print(make_matrix(new_tweets, unique_words))

#Generating a matrix for all the tweets
from sklearn.feature_extraction import CountVectorizer

#construct a bag of words matrix
#lowercase everything and remove stopwords
vectorizer = CountVectorizer(lowercase=True, stop_words="english")

matrix = vectorizer.fit_transform(tweets)
print(matrix.todense())

#applying the same method to all tweets
full_matrix = vectorizer.fit_transform(tweets["tweet"])
print(full_matrix.shape)



#adding some meta features
transform_functions = [
    lambda x: len(x),
    lambda x: x.count(" "),
    lambda x: x.count("."),
    lambda x: x.count("!"),
    lambda x: x.count("?"),
    lambda x: len(x) / (x.count(" ") + 1),
    lambda x: x.count(" ") / (x.count(".") + 1),
    lambda x: len(re.findall("\d", x)),
    lambda x: len(re.findall("[A-Z]",x)),
]

columns = []
for func in transform_functions:
    columns.append(tweets.apply(func))

#convert the meta functions to a numpy array
meta = numpy.asarray(columns).T


#adding some more features
columns = []

#convert tweet dates column to datetime
tweets_dates = pandas.to_datetime(tweets["tweets_time"])

#transform functions for datetime column
transform_functions = [
    lambda x: x.year,
    lambda x: x.month,
    lambda x: x.day,
    lambda x: x.hour,
    lambda x: x.minute,
]


#apply all functions to the datetime column
for func in transform_functions:
    columns.append(tweets_dates.apply(func))
    
#convert the meta features to a numpy array
non_nlp = numpy.asarray(columns).T

#concatenate the features together
features = numpy.hstack([non_nlp, meta])


#making predictions
from sklearn.linear_model import Ridge
import numpy
import random
'''
train_rows = 800
random.seed(1)

#shuffle the indices 
indices = list(range(features.shape[0]))
random.shuffle(indices)


#create train and test sets
train = features[indices[:train_rows], :]
test = features[indices[train_rows:], :]
train = numpy.nan_to_num(train)

#run the regression
reg = Ridge(alpha=0.1)
reg.fit(train, train)
predictions = reg.predict(test)
'''
