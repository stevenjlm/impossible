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

class listener(StreamListener):

    def on_data(self, data):
      try:
	post_id=json.loads(data)['id']
	#print post_id
	post_text=json.loads(data)['text']
	post_text=re.sub(r'\W\s', '', post_text)
	post_text=re.sub(r'(?<!\w)@\w+', '', post_text)
	print post_text
	post_rt=json.loads(data)['retweeted']
	#print post_rt
	post_creat_time=json.loads(data)['created_at']
	#print post_creat_time
	print self.test_var
	self.test_var+=1
	
	#--------------- WRITING TO DATABASE

	try: 
	    
	    tweet=[(self.test_var, post_id, post_text, post_rt, post_creat_time)]
	    
	    query = "INSERT INTO tweets VALUES (?, ?, ?, ? ,?)"
	    self.cur.executemany(query, tweet)
	    

	except lite.Error, e:
	    
	    if self.con:
		self.con.rollback()
	    
	    print 'Error %s' % e    
	    sys.exit(1)
	    
		
	if self.test_var > 100000:
	  if self.con:
	    self.con.commit()
	    self.con.close()
	  return False
	else:
	  return True
	
      except KeyError:
	sterfs='--not interesting data--'
	print sterfs
	return True
      else:
	print '!!ERROR!!'
	return False

    def on_error(self, status):
        print status



#Open database
con = None

try:
     
    con = lite.connect(database='tweets.db') 
  
    cur = con.cursor()  
    
    cur.execute("DROP TABLE IF EXISTS tweets")
    cur.execute("CREATE TABLE tweets(our_id INT PRIMARY KEY, tweet_id INT, body TEXT, retweet BOOLEAN, created DATE)")
    #query = "INSERT INTO cars (id, name, price) VALUES (%s, %s, %s)"
    #cur.executemany(query, cars)
        
    con.commit()
    

except lite.Error, e:
    
    if con:
        con.rollback()
    
    print 'Error %s' % e    
    sys.exit(1)
    
    
finally:
    
    if con:
        con.close()

#Connect to twitter
is_global=0;

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
twitterStream = Stream(auth, listener())

twitterStream.filter(track=['and'],languages=['en'])
#filter for 'and' is a hack to get languages to work