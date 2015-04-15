import urllib2
import json
from api_key import *


server_key = server_key

def getPlaceId(latitude, longitude, place_name):
	global server_key
	place_name = 'Layne'
	latitude = 30.592553
	longitude = -96.331252
	api_request = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location='+str(latitude) + ',' + str(longitude) + '&radius=500&key=' + server_key
	data = json.loads(urllib2.urlopen(api_request).read())
	#print data['results'][2]['name']
	for place in data['results']:
		#print place['name']
		if place_name in place['name']:
			#print place['place_id']
			place_id = place['place_id']
			return place_id

def getReviews(place_id):
	global server_key
	api_request = 'https://maps.googleapis.com/maps/api/place/details/json?placeid=' + place_id + '&key=' + server_key
	data = json.loads(urllib2.urlopen(api_request).read())
	server_message = ''
	#data['result']['reviews']
	for review in data['result']['reviews']:
		server_message = server_message + "<p>\"" + review['text'] + "\"</p><br><hr>"
		#print review['rating']
		#print review['text']

def main():
	getReviews(getPlaceId(1,1,'dummy'))

main()
