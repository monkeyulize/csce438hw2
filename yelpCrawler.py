from api_key import *
import time
import json
import rauth


def get_search_parameters(lat, long, term):
  #See the Yelp API for more details
  params = {}
  params["term"] = term
  params["ll"] = "{},{}".format(str(lat),str(long))
  params["radius_filter"] = "2000"
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
  data = request.json()
  session.close()
   
  return data

  
def perform_search(lat, long, term):
	params = get_search_parameters(lat, long, term)
	api_calls = []
	api_calls.append(get_results(params))
	time.sleep(1.0)
	file = open('testfile.txt', 'w+')
	file.write(str(api_calls))
	file.close

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
