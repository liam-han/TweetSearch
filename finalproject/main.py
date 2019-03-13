import json
import string
import lxml.html
import re
from urllib.request import urlopen
import urllib.request
from bs4 import BeautifulSoup
import requests
#liam
from elasticsearch import Elasticsearch
es = Elasticsearch()


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



def indexTweets(tweets):
    '''
    function that places json tweets into a new index to use Elasticsearch search engine 
    
    '''
    # create new index
    if es.indices.exists('test-index'):
    es.indices.delete(index='tweet_index')
    
    # fill index with tweeets
    count = 1
    for tweet in tweets:
        res = es.index(index="tweet_index", doc_type='tweet', id=count, body=tweet)
        res = es.get(index="tweet_index", doc_type='tweet', id=count)
        count += 1
    
    es.indices.refresh(index="tweet_index")
    
    return
    

def searchTweets():
    # input for Eli for location or whatever needed to get location information
    user_input = "Bronx, NY"
    
    while user_input != "QUIT":
        
        # QUERY SEARCH, return Size 10 of specific parameter to return matching user_input
        user_input = input("Input term to search index, or type 'QUIT' to exit:")
        res = es.search(index="tweet_index", body={"size":20, "query": {"match": { "place.full_name" : user_input }}})

        # Return total number of matches and outputs them
        print("Got %d Hits:" % res['hits']['total'])
        for hit in res['hits']['hits']:
            print(hit["_source"])
    
    return res['hits']['hits'] # LIST OF RESULTING TWEETS IN JSON INDEX


'''
Takes the multiple coordinates from a tweet geolocation and averages them out to a single coordinate
'''
def avgCoordinates(tweet):
    c1 = []
    c2 = []
    for coordinate in tweet['place']['bounding_box']['coordinates']:
        c1.append(coordinate[0])
        c2.append(coordinate[1])
    
    return [sum(c1)/len(c1), sum(c2)/len(c2)]



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
    
    
    '''
    Create the ElasticSearch index. (Requires a node to be running locally)
    takes json tweets and runs search engine.
    returns list of top query results (json index term).
    Searched tweet in json form => searched_tweet['_source']
    '''
    
    indexTweets(tweet_json)
    searched_tweets = searchTweets()
    searched_json_tweets = []
    for searched_tweet in searched_tweets:
        searched_json_tweets.append(searched_tweet['_source'])
    
    # for json_tweet in searched_json_tweets:
        # location: avgCoordinates(json_tweet['place']['coordinates'])
        # text: json_tweet['text']
    
    return

if __name__ == "__main__":
    main()