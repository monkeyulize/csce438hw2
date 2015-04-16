from api_key import *
import time
import json
import rauth


def get_search_parameters(lat, long, term):
  #See the Yelp API for more details
  params = {}
  params["term"] = term
  params["ll"] = "{},{}".format(str(lat),str(long))
  params["radius_filter"] = "200"
  params["limit"] = "1"
 
  return params

def get_results(params):
   
  session = rauth.OAuth1Session(
    consumer_key = consumer_key
    ,consumer_secret = consumer_secret
    ,access_token = access_key
    ,access_token_secret = access_secret)
     
  request = session.get("http://api.yelp.com/v2/search",params=params)
   
  #Transforms the JSON API response into a Python dictionary
  response = request.json()
  session.close()
  businesses = response.get('businesses')
  if not businesses:
    return

  data = dict([('url', businesses[0]['url']),
               ('image_url', businesses[0]['image_url']),
			   ('review_count', businesses[0]['review_count']),
               ('rating_image_url', businesses[0]['rating_img_url']),
               ('snippet_text', businesses[0]['snippet_text']),
               ('name', businesses[0]['name']),
               ('rating', businesses[0]['rating']),
               ('city', businesses[0]['location']['city'])])
   
  message_to_server = ""
  message_to_server += "<center><p>" + data['name'] + "</p></center>"
  message_to_server += "<center><img src=\"" + data['rating_image_url'] + "\" width=\"132px\" height=\"26px\"></center>"
  message_to_server += "<center><h3><b><i>" + str(data['review_count']) + "reviews</i></b></h3></center>"
  message_to_server += "<p>\"" + data['snippet_text'] + "\"</p>"
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  return message_to_server

  
def perform_search(lat, long, term):
	params = get_search_parameters(lat, long, term)
	api_calls = []
	#api_calls.append(get_results(params))
	#time.sleep(1.0)
	#file = open('testfile.txt', 'w+')
	#file.write(str(api_calls))
	#file.close
	return get_results(params)

def main():
  locations = [(30.63,-96.33)]
  api_calls = []
  for lat,long in locations:
    params = get_search_parameters(lat,long)
    api_calls.append(get_results(params))
    #rate limiting
    time.sleep(1.0)
    #print api_calls
  file = open('testfile.txt', 'w+')
  file.write(str(api_calls))
  file.close
     
  ##Do other processing

if __name__ == "__main__":
    main()
