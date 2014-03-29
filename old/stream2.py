from slistener import SListener
import time, tweepy, sys

## authentication
username = '' ## put a valid Twitter username here
password = '' ## put a valid Twitter password here
auth     = tweepy.auth.BasicAuthHandler(username, password)
api      = tweepy.API(auth)

def main():
    track = ['obama', 'romney']
 
    listen = SListener(api, 'myprefix')
    stream = tweepy.Stream(auth, listen)

    print "Streaming started..."

    try: 
        stream.filter(track = track)
    except:
        print "error!"
        stream.disconnect()

if __name__ == '__main__':
    main()
    
    
    
    
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from slistener import SListener
import time, sys


class listener(StreamListener):

    def on_data(self, data):
        print data
        return True

    def on_error(self, status):
        print status

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
api = tweepy.API(auth)
listen = SListener(api, 'myprefix')
twitterStream = Stream(auth, listener())