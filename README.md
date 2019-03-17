### Group Members:
  -Liam Han (Part 1: WebCrawler; Twitter )
  
  Used the tweepy library to access the Twitter API. Tweepy provides an example template called 'streaming.py' which
we used to stream and download tweets. We added a geo location filter by coordinates when streaming.
After retrieving the json file from the twitter api, we loaded it into python using the json library. 
Went through each tweet in the collection and checked for URLs in tweets with re.search and ran it through BeautifulSoup
for webpage titles. Created a new key and updated the json file with the webpage title.  

  -Antonius Panggabean (Part2: Retrieval)
  
  -Elijah Nicasio (Part3: Extensions[geolocation])


For this project we decided to use Twitter to get json files to use for Elastic Search.  

