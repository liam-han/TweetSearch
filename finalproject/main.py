import json
import string
import lxml.html
import re
from urllib.request import urlopen
import urllib.request
from bs4 import BeautifulSoup
import requests



def readFile(filename):
    geo_located_tweets = []

    with open(filename, "r") as f:
        for line in f.readlines():
            try:
                tweet = json.loads(line)
                geo_located_tweets.append(tweet)
            except:
                continue
    return geo_located_tweets



def collect_tweet_texts(tweets) -> []:
    '''
    Tweets are represented in json format.
    Function collects 'text' ( < 280 characters ) and truncated tweets 'full_text' ( >280 )
    Extracts URLs from tweets
    '''
    tweet_data = list()
    urls = list()
    for tweet in tweets:
        try:
            if tweet['truncated'] == True:
                tweet_data.append(tweet['extended_tweet']['full_text'].lower())
                url = re.search("(?P<url>https?://[^\s]+)", tweet['extended_tweet']['text']).group("url")
                soup = BeautifulSoup(urllib.request.urlopen(url), "lxml")
                #print(soup.title.string.lower())
            else:
                tweet_data.append(tweet['text'].lower())
                url = re.search("(?P<url>https?://[^\s]+)", tweet['text']).group("url")
                soup = BeautifulSoup(urllib.request.urlopen(url), "lxml")
                webpage_title = soup.title.string.lower()
                if "twitter" not in webpage_title:
                    print(webpage_title)
                else:
                    continue
    
        except:
            continue
   
    
    return tweet_data



def main():
    
    filename = 't_tweets.json'
    geo_located_tweets = readFile(filename)
    tweets = collect_tweet_texts(geo_located_tweets)
        

    #print(geo_located_tweets[14]['extended_tweet'])
if __name__ == "__main__":
    main()