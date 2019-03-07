import json




path = 'twitter.txt'

tweets_data = []

with open(path, "r") as f:
    for line in f:
        try:
            tweet = json.loads(line)
            tweets_data.append(tweet)
        except:
            continue
    
print(len(tweets_data))