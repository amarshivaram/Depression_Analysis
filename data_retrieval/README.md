# Data retrieval


Project titled “Detecting Early Traces of depression through Twitter User Activity” at OvGU, Magdeburg. The aim of the project was to detect early traces of depression in twitter user activity. 


### Setup

Create Twitter keys from Twitter API Dashboard. 

```bash
# Eg. run command to retrieve tweets for keyword "mentalhealth"
$ python tweet_retrieval.py --searchkey "mentalhealth" --tweetcount 2 --sinceDate "2020-05-27" --untilDate "2020-05-28" --outputFile depress_hash_1.csv 
