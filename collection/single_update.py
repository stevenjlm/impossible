#twitter connection libraries
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import tweepy
import json

#Database modules
import sqlite3 as lite
import sys
import re

sys.path.insert(0, '/home/steven/Documents/code/python')
from keys import *

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
api = tweepy.API(auth)
new_rt=api.get_status(449352950440534017)
print new_rt.text
print new_rt.id
print new_rt.retweeted
