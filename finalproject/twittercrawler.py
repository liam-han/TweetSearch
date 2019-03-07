import tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json


'''
Twitter API tokens 
'''
access_token = '2193013314-h2zCKpsu7oyZ8dhKcCMtCQHiFjm44d6BV6qH9JD'
access_token_secret = 'vJ4mG9buIYItf5m0KOOVQVw4F6mjsL27LTe3KOfBlbm5H'
consumer_key = 'BhhdUMKHuXrdKAUBQjRF8hI3q'
consumer_secret = 'D9LcFt02F68UtT118sqRsmpj1c8WCG4b3VROdUv4TPhqLAD7He'


class StdOutListener(StreamListener):
    """ 
    A basic listener that just prints received tweets to stdout.
    """
    def on_data(self, data):
        print(data)
        return True

    def on_error(self, status):
        print(status)



if __name__ == '__main__':
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    api = tweepy.API(auth)
'''
Filter twitter stream by location [San Francisco OR New York]
'''
stream.filter(locations=[-122.75,36.8,-121.75,37.8,-74,40,-73,41])



