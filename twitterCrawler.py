#!/usr/bin/env python
# -*- coding: utf-8  -*-
#encoding=utf-8

import tweepy
import time
import sys
import re
from random import randint
from api_key import *


class TwitterCrawler():
    consumer_key = consumer_key
    consumer_secret = consumer_secret
    access_key = access_key
    access_secret = access_secret
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
        metadata = self.api.search(q=query,count=num)
        print metadata
        tweets = metadata['statuses']
        tweet_list = []
        print len(tweets)
        for k in range(0, min(len(tweets), num)):
            dummy = tweets[k]['text'].encode('ascii','ignore')
            print dummy
            unicode_word=re.findall(r'\w+',dummy)
            tweet_list += [str(word) for word in unicode_word ]
        return tweet_list

def main():
    tc = TwitterCrawler()
    tc.check_api_rate_limit(900)
    tweet_list = tc.get_query_tweets('peace of earth pottery', 10)

    #print tweet_list

if __name__ == "__main__":
    main()
