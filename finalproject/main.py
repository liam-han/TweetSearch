import json
import string
import lxml.html
import re
from urllib.request import urlopen
import urllib.request
from bs4 import BeautifulSoup
import requests



def readFile(filename: 'json file'):
    geo_located_tweets = []

    with open(filename, "r") as f:
        for line in f.readlines():
            try: 
                tweet = json.loads(line)
                geo_located_tweets.append(tweet)
            except:
                continue
    return geo_located_tweets

def writeFile(tweets):
    with open('tweets.txt', 'w') as f:
        for item in tweets:
            f.write("%s\n" % item)

def updateJson(tweet_json):
    '''
    Updates read JSON file with 'has_url' and 'webpage_title' keys.
    Pretty-print
    '''
    with open('new_tweets.json', 'w') as outfile:
        json.dump(tweet_json, outfile, sort_keys = True, indent = 4)


def collect_tweet_texts(tweets) -> []:
    '''
    Tweets are represented in json format.
    Function collects 'text' ( < 280 characters ) and truncated tweets 'full_text' ( >280 )
    If tweet has URL grab webpage title and add to json file. 
    '''
    tweet_data = list()

    for tweet in tweets:
        tweet['has_url'] = False
        try:
            if tweet['truncated'] == True:
                tweet_data.append(tweet['extended_tweet']['full_text'].lower())
                url = re.search("(?P<url>https?://[^\s]+)", tweet['extended_tweet']['full_text']).group("url")
                soup = BeautifulSoup(urllib.request.urlopen(url), "lxml")
                webpage_title = soup.title.string.lower()
                if "twitter" not in webpage_title:
                    tweet['has_url'] = True
                    tweet['webpage_title'] = webpage_title

            else:
                tweet_data.append(tweet['text'].lower())
                url = re.search("(?P<url>https?://[^\s]+)", tweet['text']).group("url")
                soup = BeautifulSoup(urllib.request.urlopen(url), "lxml")
                webpage_title = soup.title.string.lower()
                if "twitter" not in webpage_title:
                    tweet['has_url'] = True
                    tweet['webpage_title'] = webpage_title
                
                else:
                    continue
    
        except:
            continue
   
    
    return tweet_data, tweets



def main():
    
    filename = 't_tweets.json'
    geo_located_tweets = readFile(filename)
    tweets = collect_tweet_texts(geo_located_tweets)
    tweet_data = tweets[0]
    tweet_json = tweets[1]
   
    '''
    Update JSON file with webpage titles.
    ['has_url] = False by default. 
    if tweet['has_url'] = True, add ['webpage_title] to tweet. 
    '''
    updateJson(tweet_json)
    
    '''
    Writes tweets into 'tweets.txt' file line by line.
    '''
    writeFile(tweet_data)

    
if __name__ == "__main__":
    main()