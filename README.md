### Group Members:
  -Liam Han (Part 1: WebCrawler; Twitter )
  
  Used the tweepy library to access the Twitter API. Tweepy provides an example template called 'streaming.py' which
we used to stream and download tweets. We added a geo location filter by coordinates when streaming.
After retrieving the json file from the twitter api, we loaded it into python using the json library. 
Went through each tweet in the collection and checked for URLs in tweets with re.search and ran it through BeautifulSoup
for webpage titles. Created a new key and updated the json file with the webpage title.  

  -Antonius Panggabean (Part2: Retrieval)
  
  -Elijah Nicasio (Part3: Extensions[geolocation])
  
  To run everything altogether, you must have python and virtualenv. Virtualenv is not necessary, however, if you lack the libraries necessary to run our program (which you most likely will), virutalenv simply allows you to run it without installing all the required libraries. First, activate the virtual environment by running ‘source /loc/activate’. Activate is located in webApp/env/scripts. Then, go to the webapp folder and run ‘python manage.py runserver’. Connect to the website, which is locally hosted at ‘http://127.0.0.1:8000/’, and our program should be working. Enter the query you which to search for, and the program will return a list of tweets from California and New York in a ranked list. Keep in mind that this all assumes that indexing has already been done as per the part 2, in elasticsearch.
  The libraries used for this part were mainly django, folium, and bootstrap. For more info, please look at the final project report included in this repo.
  


For this project we decided to use Twitter to get json files to use for Elastic Search.  

