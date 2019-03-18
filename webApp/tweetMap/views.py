# tweetMap/views.py
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.gis.geoip2 import GeoIP2

from folium.plugins import Search

import folium
import os
from . import tweetIndex

tempVar = 1

def index(request):
	# Converts user's ip to lat lon
	geoDir = (os.path.join(os.path.dirname(__file__), 'GEOIP_PATH/GeoLite2-City_20190305/GeoLite2-City.mmdb'))
	g = GeoIP2(geoDir)
	ip = request.META.get('REMOTE_ADDR', None)

	# starting location
	loc = ''

	if ip == '127.0.0.1':
		# Default is UCR
		loc = [33.9737, -117.3281]
	else:
		loc = g.lat_lon(ip)

	# displays map
	m = folium.Map(location=loc, zoom_start=5)

	# Tweets
	#tweets = [[33.9550573,-117.38889023, 'Alpha'], [34.05139929,-117.19333151, 'Beta'], [33.88303718,-117.20156382, 'Gamma'], [34.03881436,-117.31486311,'Delta']]
	#tweets = {'1': [33.9550573,-117.38889023], '2': [34.05139929,-117.19333151], '3': [33.88303718,-117.20156382], '4': [34.03881436,-117.31486311]}
	#tweets = {[33.9550573,-117.38889023]: '1', [34.05139929,-117.19333151]: '2', [33.88303718,-117.20156382]: '3', [34.03881436,-117.31486311]: '4'}

	tweetLoc = (os.path.join(os.path.dirname(__file__), 'tweets/t_tweets.json'))
	tweetJson = tweetIndex.readFile(tweetLoc)
	tweets = tweetIndex.collect_tweet_texts(tweetJson)
	tweet_data = tweets[0]
	tweet_json = tweets[1]

	tweetIndex.updateJson(tweet_json)

	tweetIndex.indexTweets(tweet_json)


	#tweetGeo = folium.GeoJson(tweets).add_to(m)

	"""for tweet in tweets:
					folium.Marker(
						location=[tweet[0],tweet[1]],
						popup=tweet[2]
					).add_to(m)"""

	# Searchbar
	"""tweetSearch = Search(
					layer=tweetGeo,
					geom_type='Point',
					placeholder="Search Tweets",
					#search_label='popup'
				).add_to(m)"""

	# puts map to html
	tweetIndexFileLoc = (os.path.join(os.path.dirname(__file__), 'templates/foliumMap.html'))
	m.save(tweetIndexFileLoc)

	tweetIndexFile = open(tweetIndexFileLoc)

	return render(request, 'index.html')

def submit(request):

	query = 'dasdasdasdasdas'

	if 'tweetQuery' in request.GET:
		query = request.GET['tweetQuery']

	tweetListFileLoc = (os.path.join(os.path.dirname(__file__), 'templates/tweetList.html'))

	#query = "tuna"

	#print(request.GET)
	print(tempVar)

	return render(request, 'tweetList.html', {"query": query})

def search(request):

	query = ''

	if 'tweetQuery' in request.GET:
		query = request.GET['tweetQuery']

	searched_tweets = tweetIndex.searchTweets(query)
	temp = searched_tweets

	results = []

	resultExists = True

	if temp:
		resultExists = True

		for re in temp:
			#results.append(re.keys())
			
			if re['_source']['geo'] != None:
				#results.append(re['_source']['geo']['coordinates'])	
				results.append((re['_score'], re['_source'], re['_source']['geo']['coordinates']))
			else:
				#results.append(re['_source']['place']['bounding_box']['coordinates'])
				results.append((re['_score'], re['_source'], tweetIndex.avgCoordinates(re['_source'])))

		m = folium.Map(location=(results[0][2][1], results[0][2][0]), zoom_start=5)

		for index, item in enumerate(results):
			if abs(item[2][1]) > 60: 
				folium.Marker(
				location=[item[2][0],item[2][1]],
				popup=str(index + 1)
				).add_to(m)
			else:
				folium.Marker(
					location=[item[2][1],item[2][0]],
					popup=str(index + 1)
				).add_to(m)

		tweetIndexFileLoc = (os.path.join(os.path.dirname(__file__), 'templates/foliumMap.html'))
		m.save(tweetIndexFileLoc)
	else:
		resultExists = False

		m = folium.Map(location=[33.9737, -117.3281], zoom_start=5)
		tweetIndexFileLoc = (os.path.join(os.path.dirname(__file__), 'templates/foliumMap.html'))
		m.save(tweetIndexFileLoc)

	return render(request, 'search.html', {"query": query, "results":results, "resultExists":resultExists})