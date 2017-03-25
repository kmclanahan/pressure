
positive_words = ['awesome', 'good', 'nice', 'super', 'fun', 'delightful', 'great', 'enjoy', 'like']
negative_words = ['awful', 'lame', 'horrible', 'dreadful', 'bad', 'terrible', 'disaster', 'crisis', 'accident', '']

#we could have them in files
files = ['negative_tweets.txt', 'positive_tweets.txt', 'data_tweets.txt']

#path = '/path_to_tweets/'

for file_name in files:
    urllib.urlretrieve(path+file_name,file_name)
tweets = open("data_tweets.txt").read()
tweets_list = tweets.split('\n')

pos_sent = open("positive.txt").read()
positive_words = pos_sent.split('\n')
positive_counts = []

neg_sent = open("negative.txt").read()
negative_words = neg_sent.split('\n')
negative_counts = []

for tweets in tweets_list:
    positive_counter = 0
    negative_counter = 0
    
    tweets_processed = tweet.lower()
    
    for p in list(punctuation):
        tweets_processed = tweet_processed.replace(p,'')
        
    words = tweets_processed.split(' ')
    word_count = len(words)
    for word in words:
        if word in positive_words:
            positive_counter = positive_counter + 1
        elif word in negative_words:
            negative_counter = negative_counter + 1
            
    positive_counts.append(positive_counter/word_count)
    negative_counts.append(negative_counter/word_count)
    
print(len(positive_words))
print(len(negative_words))

output = zip(tweets_list, positive_counts, negative_counts)
writer = csv.writer(open('tweet_sentiment.csv', 'wb'))
writer.writerows(output)




