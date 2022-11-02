# -*- coding: utf-8 -*-
"""
Created on Thu May 28 08:48:07 2020

@author: Amar
"""

import tweepy
import pandas as pd
import argparse
from datetime import datetime


start=datetime.now()


parser = argparse.ArgumentParser()
parser.add_argument("--searchkey", type=str,help="store the search key")
parser.add_argument("--tweetcount", type=int,help="store the tweet count to be retrieved")
parser.add_argument("--outputFile", type=str,help="store the name of output file")
#parser.add_argument("--sinceDate", type=str,help="store the start date")
#parser.add_argument("--untilDate", type=str,help="store the end date")

args = parser.parse_args()

#"2018-11-16"
keysearch = args.searchkey
retrievalCount = args.tweetcount
outputFile = args.outputFile
date_since = "2021-11-15"
date_until = "2022-02-15"

## Create Twitter keys from Twitter API Dashboard. 
consumer_key = ########### create consumer key
consumer_secret = ########### create consumer secret
access_key = ########### create access key
access_secret = ########### create access secret


auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)


#print("Retrieval starts")
#tweets = tweepy.Cursor(api.search, q=keysearch, lang = 'en', tweet_mode = 'extended',since = date_since, until = date_until).items(retrievalCount)
#print("Retrieval ends")
 
#print("Retrieval starts")
#tweets = tweepy.Cursor(api.user_timeline, screen_name=keysearch, lang = 'en', include_rts = False, tweet_mode = 'extended',count = retrievalCount,since = date_since, until = date_until).items(retrievalCount)
#print("Retrieval ends")


print("Retrieval starts")
#tweets = tweepy.Cursor(api.search, q=keysearch, lang = 'en', tweet_mode = 'extended',since = date_since, until = date_until, include_rts = False).items(retrievalCount)
tweets = tweepy.Cursor(api.user_timeline, screen_name=keysearch, lang = 'en', include_rts = False, tweet_mode = 'extended',count = retrievalCount).items(retrievalCount)
#tweets = tweepy.Cursor(api.user_timeline, screen_name=keysearch, lang = 'en', include_rts = False, tweet_mode = 'extended',since = date_since, until = date_until).items()
print("Retrieval ends")




   
cols = ["twittername","accountname","twitterid","timestamp","tweets","location","description","retweet_count","favorite_count"]


#print("Test---------------------")
#for tweet in tweets:
#    print(tweet)

tweet_data = [[tweet.user.screen_name, tweet.user.name, tweet.user.id, tweet.created_at, tweet.full_text, tweet.user.location, tweet.user.description, tweet.retweet_count, tweet.favorite_count] for tweet in tweets]


tweet_df = pd.DataFrame(data=tweet_data, columns=cols)


tweet_df.to_csv(outputFile, encoding='utf-8', index=False)
print("Time taken for run: ",datetime.now()-start)
print("File created and stored.. ")