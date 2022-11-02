# -*- coding: utf-8 -*-
"""
tweet_clean_tp : Does cleaning of tweet by removing the hashtags mentions links and emotions 
extract_emoji : extracts emojis from the tweet
retrieve hashtags: retrieves the hashtags
retrieve_mentions : retrieves the mentions
retrieve_urls : retieves the urls
stopword_removal : removes the stopwords
pos_tags : retrieves the words with specific pos tags
lemmatise : lemmatises the tweet
porter_stemming : performs the porter stemming for the tweet
check_tweet_comment: performs checks to see if the tweet is a novel tweet or a comment COMMENT-->0 TWEET-->1

Eg of calling method:
    
    cleanData = twitterDataRaw["tweets"].apply(tweet_clean_tp)
    
    where you pass the pandas Series as the data using the apply function to call the function to perform. 
    
    
"""
import tweepy
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener

import re #regular expression
import string
import preprocessor as p
from stop_words import get_stop_words
import nltk
from nltk.corpus import stopwords,wordnet
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer,PorterStemmer
import emoji
from spellchecker import SpellChecker
import contractions


from empath import Empath
lexicon = Empath()
spell = SpellChecker()


class AntonymReplacer(object):
    def replace(self, word, pos=None):
        antonyms = set()
        for syn in wordnet.synsets(word, pos=pos):
            for lemma in syn.lemmas():
                for antonym in lemma.antonyms():
                    antonyms.add(antonym.name())
        if len(antonyms) == 1:
            return antonyms.pop()
        else:
            return None
        
        
    def replace_negations(self, sent):
        i, l = 0, len(sent)
        words = []
        while i < l:
            word = sent[i]
            if word == 'not' and i+1 < l:
                ant = self.replace(sent[i+1])
                if ant:
                    words.append(ant)
                    i += 2
                    continue
            words.append(word)
            i += 1
        return words


replacer = AntonymReplacer()


def connect_Twitter(prop):
    
    
    
    auth = tweepy.OAuthHandler(prop['TwitterCredentials']['consumer_key'], prop['TwitterCredentials']['consumer_secret'])
    auth.set_access_token(prop['TwitterCredentials']['access_key'], prop['TwitterCredentials']['access_secret'])
    api = tweepy.API(auth)
    
    
    return api



#HappyEmoticons
emoticons_happy = set([
    ':-)', ':)', ';)', ':o)', ':]', ':3', ':c)', ':>', '=]', '8)', '=)', ':}',
    ':^)', ':-D', ':D', '8-D', '8D', 'x-D', 'xD', 'X-D', 'XD', '=-D', '=D',
    '=-3', '=3', ':-))', ":'-)", ":')", ':*', ':^*', '>:P', ':-P', ':P', 'X-P',
    'x-p', 'xp', 'XP', ':-p', ':p', '=p', ':-b', ':b', '>:)', '>;)', '>:-)',
    '<3'
    ])
    
    
# Sad Emoticons
emoticons_sad = set([
    ':L', ':-/', '>:/', ':S', '>:[', ':@', ':-(', ':[', ':-||', '=L', ':<',
    ':-[', ':-<', '=\\', '=/', '>:(', ':(', '>.<', ":'-(", ":'(", ':\\', ':-c',
    ':c', ':{', '>:\\', ';('
    ])
    
    
    
emoticons = emoticons_happy.union(emoticons_sad)


#Emoji patterns
emoji_pattern = re.compile("["
         u"\U0001F600-\U0001F64F"  # emoticons
         u"\U0001F300-\U0001F5FF"  # symbols & pictographs
         u"\U0001F680-\U0001F6FF"  # transport & map symbols
         u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
         u"\U00002702-\U000027B0"
         u"\U000024C2-\U0001F251"
         "]+", flags=re.UNICODE)
    
    
    
def tweet_clean_tp(rawData):

    rawData = p.clean(rawData)
    
    return rawData

def tweet_parse_tp(text):
    
    parse_df = p.parse(text)
    
    return parse_df
    
def extract_emojis(s):
    return ''.join(c for c in s if c in emoji.UNICODE_EMOJI)

def retrieve_hashtags(tweet):
    
    hashtags = [i  for i in tweet.split() if i.startswith("#") ]
    return hashtags

def retrieve_mentions(tweet):
    mentions = re.findall(r"@([a-zA-Z0-9]{1,15})", tweet)
    return mentions

def retrieve_urls(tweet):
    urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', tweet)
    
    return urls

def url_token(tweet):
    
    
    tweet=re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', r'[URL]', tweet) #replaces links with "URL"
    
    return tweet

def retrieve_emotions(text):
    full_emotions = lexicon.analyze(text, normalize=True)

    actual_emotions = {}
    for k, v in full_emotions.items():
        if v>0:
            actual_emotions[k] = v

    return actual_emotions


def stopword_removal(tweet):

    stop_words = list(get_stop_words('en'))         
    nltk_stopwords = list(stopwords.words('english'))   
    stop_words.extend(nltk_stopwords)
    stop_words = list(set(stop_words))

    
    #after tweepy preprocessing the colon symbol left remain after      #removing mentions
    tweet = re.sub(r':', '', tweet)
    tweet = re.sub(r'‚Ä¶', '', tweet)
    
    
    #replace consecutive non-ASCII characters with a space
    tweet = re.sub(r'[^\x00-\x7F]+',' ', tweet)
    
    #remove emojis from tweet
    tweet = emoji_pattern.sub(r'', tweet)

    word_tokens = word_tokenize(tweet)
    
    #filter using NLTK library append it to a string
#    filtered_tweet = [w for w in word_tokens if not w in stop_words]
    filtered_tweet = []
    
    # looping through conditions
    for w in word_tokens:
        #check tokens against stop words , emoticons and punctuations
        if w not in stop_words and w not in emoticons and w not in string.punctuation:
            filtered_tweet.append(w)

    filtered_tweet = (" ".join(filtered_tweet))
    return filtered_tweet
    
def pos_tags(tweet):
    
    tweet_tokens = word_tokenize(tweet)
    
    tagged = nltk.pos_tag(tweet_tokens)
    
#    print(tagged)
    verbs_list = []
    nouns_list = []
    adjectives_list = []
    adverbs_list = []
    
    for i in range(len(tagged)):
        if tagged[i][1] == 'JJ' or tagged[i][1] == 'JJR' or tagged[i][1] == 'JJS':
            adjectives_list.append(tagged[i][0])
#    for i in range(len(tagged)):
        elif tagged[i][1] == 'RB' or tagged[i][1] == 'RBR' or tagged[i][1] == 'RBS':
            adverbs_list.append(tagged[i][0])
#    for i in range(len(tagged)):
        elif tagged[i][1] == 'NN' or tagged[i][1] == 'NNS' or tagged[i][1] == 'NNP' or tagged[i][1] == 'NNPS':
            nouns_list.append(tagged[i][0])
#    for i in range(len(tagged)):
        elif tagged[i][1] == 'VB' or tagged[i][1] == 'VBD' or tagged[i][1] == 'VBG' or tagged[i][1] == 'VBN' or tagged[i][1] == 'VBP' or tagged[i][1] == 'VBZ':
            verbs_list.append(tagged[i][0])
    
    
    pos_tag_list = verbs_list + nouns_list + adjectives_list + adverbs_list
    
#    print(pos_tag_list)
    pos_tag_list = (" ".join(pos_tag_list))

    return pos_tag_list



def lemmatise(tweet):
    
    tweet_tokens = word_tokenize(tweet)
    wordnet_lemmatizer = WordNetLemmatizer()
    lemmatised_tweet = [wordnet_lemmatizer.lemmatize(x) for x in tweet_tokens]

    lemmatised_tweet = (" ".join(lemmatised_tweet))
    return lemmatised_tweet


def porter_stemming(tweet):
    
    tweet_tokens = word_tokenize(tweet)
    ps= PorterStemmer()
    
    stemmed_tweet = [ps.stem(x) for x in tweet_tokens]

    stemmed_tweet = (" ".join(stemmed_tweet))
    return stemmed_tweet


def spell_check(tweet):
    correct_word = []
    mispelled_word = tweet.split()
    for word in mispelled_word:
        correct_word.append(spell.correction(word))
        
    return ' '.join(correct_word)

def fix_contractions(tweet):
    

    fixed_tweet = contractions.fix(tweet)
    
    return fixed_tweet

def check_tweet_comment(tweet):
    """
    performs checks to see if the tweet is a novel tweet or a comment COMMENT-->0 TWEET-->1

    """
    
    
    first_word = tweet.split(' ', 1)[0]
  
    res = re.search('@(\w+)', first_word)
  
    if not res:
        return 1
    else:  
        return 0

def replace_negations_antonyms(tweet):
    
    tweet_tokens = word_tokenize(tweet)

    replaced_tweet = replacer.replace_negations(tweet_tokens)
    
    replaced_tweet = (" ".join(replaced_tweet))
    return replaced_tweet