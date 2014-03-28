from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import tweepy
import json

sys.path.insert(0, '/home/steven/Documents/code/python')
from keys import *

class listener(StreamListener):

    def on_data(self, data):
      #try:
	#sterfs=json.loads(data)['text']
	#print sterfs
	#sterfs=json.loads(data)['retweeted']
	#print sterfs
	#return True
      #except KeyError:
	#sterfs='fff'
	#print sterfs
	#return True
      #else:
	#print 'problem'
	#return False
      print data
      return False

    def on_error(self, status):
        print status

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
twitterStream = Stream(auth, listener())
twitterStream.filter(track=['and'],languages=['en'])