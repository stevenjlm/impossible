import oauth2 as oauth
import json
 
sys.path.insert(0, '/home/steven/Documents/code/python')
from keys import *
 
#now we login in our app
consumer = oauth.Consumer(key=CONSUMER_KEY, secret=CONSUMER_SECRET)
access_token = oauth.Token(key=ACCESS_KEY, secret=ACCESS_SECRET)
client = oauth.Client(consumer, access_token)
 
#we get the timeline json
timeline_endpoint = "https://stream.twitter.com/1/statuses/sample.json"
response, data = client.request(timeline_endpoint)
 
#we load it in our variable
tweets = json.loads(data)
 
#print first tweet
print tweets