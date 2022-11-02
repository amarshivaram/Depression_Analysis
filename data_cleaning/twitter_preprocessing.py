# -*- coding: utf-8 -*-
"""
Created on Sun September 20 15:43:31 2020

@author: Amar
"""

import pandas as pd # data processing
from twitter_program import tweet_clean_tp,clean_tweets,retrieve_hashtags,retrieve_mentions,retrieve_urls,extract_emojis



### insert data path here
datapath_dep = r"D:\Workspace\OVGU\SM_Depression\src\allTweets_dep_new.csv"
datapath_nondep = r"D:\Workspace\OVGU\SM_Depression\src\allTweets_nondep_new.csv"
twitterDataRaw_dep = pd.read_csv(datapath_dep)

twitterDataRaw_depcolumn = list(twitterDataRaw_dep.columns)
twitterDataRaw_dep = twitterDataRaw_dep.reset_index(drop=True)
#twitterDataRaw = twitterDataRaw.head(50)

twitterDataRaw_dep['depressed'] = twitterDataRaw_dep['depressed'].fillna('').apply(str)

cleanData = twitterDataRaw_dep["depressed"].apply(tweet_clean_tp)




cleanData = cleanData.apply(clean_tweets)

hashtags = twitterDataRaw_dep["depressed"].apply(retrieve_hashtags)
mentions = twitterDataRaw_dep["depressed"].apply(retrieve_mentions)
urls = twitterDataRaw_dep["depressed"].apply(retrieve_urls)
emojis = twitterDataRaw_dep["depressed"].apply(extract_emojis)
#print("Printing clean data")
#print(cleanData)


cleanedDf_dep = pd.DataFrame()
cleanedDf_dep["tweet"] = twitterDataRaw_dep["depressed"]
cleanedDf_dep["cleaned_tweet"] = cleanData
cleanedDf_dep["hashtags"] = hashtags
cleanedDf_dep["mentions"] = mentions
cleanedDf_dep["emojis"] = emojis
cleanedDf_dep["urls"] = urls


cleanedDf_dep.to_csv("cleaned_depressed.csv",index=False)





twitterDataRaw_nondep = pd.read_csv(datapath_nondep)

twitterDataRaw_nondepcolumn = list(twitterDataRaw_nondep.columns)
twitterDataRaw_nondep = twitterDataRaw_nondep.reset_index(drop=True)
#twitterDataRaw = twitterDataRaw.head(50)

twitterDataRaw_nondep['non_depressed'] = twitterDataRaw_nondep['non_depressed'].fillna('').apply(str)

cleanData = twitterDataRaw_nondep["non_depressed"].apply(tweet_clean_tp)




cleanData = cleanData.apply(clean_tweets)

hashtags = twitterDataRaw_nondep["non_depressed"].apply(retrieve_hashtags)
mentions = twitterDataRaw_nondep["non_depressed"].apply(retrieve_mentions)
urls = twitterDataRaw_nondep["non_depressed"].apply(retrieve_urls)
emojis = twitterDataRaw_nondep["non_depressed"].apply(extract_emojis)
#print("Printing clean data")
#print(cleanData)


cleanedDf_nondep = pd.DataFrame()
cleanedDf_nondep["tweet"] = twitterDataRaw_nondep["non_depressed"]
cleanedDf_nondep["cleaned_tweet"] = cleanData
cleanedDf_nondep["hashtags"] = hashtags
cleanedDf_nondep["mentions"] = mentions
cleanedDf_nondep["emojis"] = emojis
cleanedDf_nondep["urls"] = urls


cleanedDf_nondep.to_csv("cleaned_nondepressed.csv",encoding="utf-8",index=False)










####E EMPATH ANALYSE EMOTIONS
#emotions = twitterDataRaw["tweets"].apply(retrieve_emotions)
#cleanedDf["emotions"] = emotions
#################################################
    
