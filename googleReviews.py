import urllib2
import json
from api_key import *


#server_key = server_key

def findStar(rating):
    # Returns image that correlates with the star rating given by a review
    return{
        1 : '''<img class="smallstars" src="http://i.imgur.com/B0HLLlb.png" width="100px" height="20px" align="right"><br><hr>''',
        2 : '''<img class="smallstars" src="http://i.imgur.com/lIx0WDU.png" width="100px" height="20px" align="right"><br><hr>''',
        3 : '''<img class="smallstars" src="http://i.imgur.com/q3tM7DV.png" width="100px" height="20px" align="right"><br><hr>''',
        4 : '''<img class="smallstars" src="http://i.imgur.com/Skq7xBD.png" width="100px" height="20px" align="right"><br><hr>''',
        5 : '''<img class="smallstars" src="http://i.imgur.com/dvh7sU5.png" width="100px" height="20px" align="right"><br><hr>'''
    }.get(rating, 'No Rating Found')

def getPlaceId(latitude, longitude, place_name):
    # Gets the PlaceID from google maps
    #global server_key
    api_request = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location='+str(latitude) + ',' + str(longitude) + '&radius=500&key=' + server_key
    data = json.loads(urllib2.urlopen(api_request).read())
    for place in data['results']:
        # You must pass the place name to the function in order to find the placeID
        if place_name in place['name']:
            place_id = place['place_id']
            return place_id

def getReviews(place_id):
    # Returns a list of reviews/ratings in html markup form
    #global server_key
    api_request = 'https://maps.googleapis.com/maps/api/place/details/json?placeid=' + place_id + '&key=' + server_key
    data = json.loads(urllib2.urlopen(api_request).read())
    server_message = ''
    if not 'reviews' in data['result']:
        return "No reviews"
    for review in data['result']['reviews']:
        server_message = server_message + "<p>" + review['text'] + "</p>" + findStar(review['rating'])
    return server_message




'''<p>"For $5, you get 5 chicken fingers, fries, coleslaw, texas toast AND their awesome mustard/bbq dipping sauce."</p>
   <img class="smallstars" src="img/example_5_stars.png" width="100px" height="20px" align="right"><br>
   <hr>
            '''
