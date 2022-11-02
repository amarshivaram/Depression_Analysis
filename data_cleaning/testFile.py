# -*- coding: utf-8 -*-
"""
Created on Sun May 10 15:43:31 2020

@author: Amar
"""

import pandas as pd # data processing
import os
from configparser import ConfigParser
from twitter_program import connect_Twitter,tweet_clean_tp,tweet_parse_tp,stopword_removal,retrieve_hashtags,retrieve_mentions,retrieve_urls,retrieve_emotions,extract_emojis,pos_tags,lemmatise,porter_stemming,spell_check,fix_contractions,replace_negations_antonyms,url_token
import datetime
import csv
import tweepy

import re

prop = ConfigParser()

#Reading the configuration file

prop.read("properties.ini")    
    



data_directory = prop['DatasetDirectory']['filepath']
filename = prop['DatasetDirectory']['rawData']




twitterDataRaw = pd.read_csv(r"D:\Workspace\OVGU\SM_Depression\src\depTweetsOrderedByDateTimeWindow.csv",encoding="utf-8")




#    print(data_directory)
twitterDataRaw = pd.read_csv(data_directory+filename)
twitterDataRaw.dropna(subset = ['timestamp'],inplace=True) 

#twitterDataRaw = twitterDataRaw[twitterDataRaw['lang']=='en']
twitterDatacolumn = list(twitterDataRaw.columns)
twitterDataRaw = twitterDataRaw.reset_index(drop=True)
# twitterDataRaw = twitterDataRaw.head(50)

twitterDataRaw['tweets'] = twitterDataRaw['tweets'].fillna('').apply(str)

twitterDataHead = twitterDataRaw.head(50)


def check_tweet_comment(tweet):
    
    
    first_word = tweet.split(' ', 1)[0]
  
    res = re.search('@(\w+)', first_word)
  
    if not res:
        return 1
    else:
  
        return 0

twitterDataHead['check_tweet_comment'] = twitterDataHead['tweets'].apply(check_tweet_comment)
# twitterDataRaw['tweets_url_token'] = twitterDataRaw['tweets'].apply(url_token)
# twitterDataHead['links'] = twitterDataHead['tweets'].apply(retrieve_urls)
# twitterDataRaw['cleanData'] = twitterDataRaw['tweets_url_token'].apply(tweet_clean_tp)

# twitterDataRaw.to_csv("depTweetsOrderedByDateTimeWindowURLTokens.csv",encoding="utf-8",index=False, date_format='%Y-%m-%d %H:%M')




contractions_fix = twitterDataRaw["tweets"].apply(fix_contractions)
cleanData = contractions_fix.apply(tweet_clean_tp)
negations_replaced = cleanData.apply(replace_negations_antonyms)




clean_stopword_removed = cleanData.apply(stopword_removal)

hashtags = twitterDataRaw["tweets"].apply(retrieve_hashtags)
mentions = twitterDataRaw["tweets"].apply(retrieve_mentions)
urls = twitterDataRaw["tweets"].apply(retrieve_urls)
emojis = twitterDataRaw["tweets"].apply(extract_emojis)
pos_cleaned_tweet = cleanData.apply(pos_tags)
lemmatised_tweet = cleanData.apply(lemmatise)
porter_stemmed_tweet = cleanData.apply(porter_stemming)
spell_checked_tweet = cleanData.apply(spell_check)


#print("Printing clean data")
#print(cleanData)


cleanedDf = pd.DataFrame()
cleanedDf["tweet"] = twitterDataRaw["tweets"]
cleanedDf["contractions_fix"] = contractions_fix
cleanedDf["cleaned_tweet"] = cleanData
cleanedDf["negations_replaced"] = negations_replaced
cleanedDf["clean_stopword_removed"] = clean_stopword_removed
cleanedDf["pos_cleaned_tweet"] = pos_cleaned_tweet
cleanedDf["spell_checked_tweet"] = spell_checked_tweet
cleanedDf["lemmatised_tweet"] = lemmatised_tweet
cleanedDf["porter_stemmed_tweet"] = porter_stemmed_tweet
cleanedDf["hashtags"] = hashtags
cleanedDf["mentions"] = mentions
cleanedDf["emojis"] = emojis
cleanedDf["urls"] = urls

cleanedDf.isnull().sum()

cleanedDf.to_csv("cleaned_sample.csv",encoding="utf-8",index=False)

####E EMPATH ANALYSE EMOTIONS
#emotions = twitterDataRaw["tweets"].apply(retrieve_emotions)
#cleanedDf["emotions"] = emotions
#################################################
    
