#!/usr/bin/env python
# -*- coding: utf-8  -*-
#encoding=utf-8

import tweepy
import time
import sys
import re
import random
from random import randint
from api_key import *


class TwitterCrawler():
    consumer_key = t_consumer_key
    consumer_secret = t_consumer_secret
    access_key = t_access_key
    access_secret = t_access_secret
    auth = None
    api = None

    def __init__(self):
        self.auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        self.auth.set_access_token(self.access_key, self.access_secret)
        self.api = tweepy.API(self.auth, parser=tweepy.parsers.JSONParser())
        self.api.rate_limit_status()

    def re_init(self):
        self.auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        self.auth.set_access_token(self.access_key, self.access_secret)
        self.api = tweepy.API(self.auth, parser=tweepy.parsers.JSONParser())

    def check_api_rate_limit(self, sleep_time):
        try:
            rate_limit_status = self.api.rate_limit_status()
        except Exception as error_message:
            if error_message['code'] == 88:
                "Sleeping for %d seconds." %(sleep_time)
                rate_limit_status['resources']['statuses']
                time.sleep(sleep_time)

        while rate_limit_status['resources']['statuses']['/statuses/user_timeline']['remaining'] < 10:
            "Sleeping for %d seconds." %(sleep_time)
            rate_limit_status['resources']['statuses']
            time.sleep(sleep_time)
            rate_limit_status = self.api.rate_limit_status()
        rate_limit_status['resources']['statuses']['/statuses/user_timeline']

    def crawl_user_profile(self, user_id):
        self.check_api_rate_limit(900)
        try:
            user_profile = self.api.get_user(user_id)
        except:
            return None
        return user_profile

    def crawl_user_tweets(self, user_id, count):
        self.check_api_rate_limit(900)
        try:
            tweets = self.api.user_timeline(user_id, count = count)
        except:
            tweets = None
        tried_count = 0
        while len(tweets) < count:
            try:
                tweets.extend(self.api.user_timeline(user_id, count = count))
            except:
                pass
            tried_count += 1
            if tried_count == 3:
                break
        return tweets[:count]

    def get_query_tweets(self, query, num):
        self.check_api_rate_limit(900)
        print(query)
        metadata = self.api.search(q=query,count=num)
        #print (metadata)
        tweets = metadata['statuses']
        tweet_list = []
        #print (len(tweets))
        for k in range(0, min(len(tweets), num)):
            dummy = tweets[k]['text'].encode('utf-8','ignore')
            #print dummy
            #unicode_word=re.findall(r'\w+',dummy)
            #tweet_list += [str(word) for word in unicode_word ]
            tweet_list.append(dummy)
        return tweet_list

def get_tweets(query):
    tc = TwitterCrawler()
    tc.check_api_rate_limit(900)
    tweet_list = tc.get_query_tweets(query, 10)
    blue_egg = "http://i.imgur.com/WR9koIb.png"
    green_egg = "http://i.imgur.com/3Raytqi.png"
    orange_egg = "http://i.imgur.com/1oMBqHq.jpg"
    purple_egg = "http://i.imgur.com/ULG3PXN.png"
    red_egg = "http://i.imgur.com/BwWYlGm.png"
    tweet_eggs = [ blue_egg, green_egg, orange_egg, purple_egg, red_egg ]
    
    html_a = '''<li class="  h-entry tweet  with-expansion  customisable-border" data-tweet-id="587760189970886656" data-rendered-tweet-id="587760189970886656" data-scribe="component:tweet">
                    <div class="header">
                    <img class="u-photo avatar" alt="" src='''
                    #egg_picture
    html_b =    ''' data-src-2x="" data-scribe="element:avatar">
                    </div>
                    <div class="e-entry-content">
                    <p class="e-entry-title">'''
                    #tweet
    html_c =        '''</p>
                    </div>

                    <div class="footer customisable-border" data-scribe="component:footer">
                    <span class="stats-narrow"><span class="stats" data-scribe="component:stats">
                    </span></span>
                    <ul class="tweet-actions" role="menu" aria-label="Tweet actions" data-scribe="component:actions">
                    <li><a href="" class="reply-action web-intent" title="Reply" data-scribe="element:reply"><i class="ic-reply ic-mask"></i><b>Reply</b></a></li>
                    <li><a href="" class="retweet-action web-intent" title="Retweet" data-scribe="element:retweet"><i class="ic-retweet ic-mask"></i><b>Retweet</b></a></li>
                    <li><a href="" class="favorite-action web-intent" title="Favorite" data-scribe="element:favorite"><i class="ic-fav ic-mask"></i><b>Favorite</b></a></li>
                    </ul>
                    <span class="stats-wide"><b>· </b><span class="stats" data-scribe="component:stats">
                    <a href="" title="View Tweet on Twitter" data-scribe="element:favorite_count">
                    <span class="stats-favorites">
                    <strong>1</strong> favorite
                    </span>
                    </a>
                    </span></span>
                    </div>
                    </li>'''
    
    #print tweet_list
    message_to_server = ""
    if not tweet_list:
        return "no tweets"
    else:
    #print(tweet_list)
        for tweet in tweet_list:
            message_to_server = message_to_server + html_a + random.choice(tweet_eggs) + html_b + str(tweet) + html_c

        return message_to_server
    
    #Send to server

#if __name__ == "__main__":
#    main()
