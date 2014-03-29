#twitter connection libraries
#	IMPORTANT: This script will not work with
#	the standard tweepy files. Check the
#	../tweepy-mods directory for the replacement
#	scripts.
from tweepy import Stream
from tweepy import OAuthHandler

#Database modules
import sqlite3 as lite

import sys
sys.path.insert(0, '/home/steven/Documents/code/python')
from keys import *

#============================================================
#Should be in a seperate file..
from tweepy.streaming import StreamListener
import tweepy

import json
import re

class listener(StreamListener):
  
    def __init__(self):
      self.tweet_count = 0

    def on_data(self, data):
      #Test if this is an actual tweet
      try:
	post_text=json.loads(data)['text']
	
	#Find out if the tweet is new or retweeted
	try:
	  post_rts=json.loads(data)['retweeted_status']
	  #Retweet!
	  retweeted_status=True
	except KeyError:
	  #New tweet!
	  retweeted_status=False
	  
	#Find out if the tweet is a reply
	post_res=json.loads(data)['in_reply_to_status_id']
	print post_res
	if post_res==None:
	  is_response=False
	else:
	  #New thread!
	  is_response=True
	  
	

	self.write_to_db(data,retweeted_status, is_response)
	      
	if self.tweet_count > 10000:
	  if self.con:
	    self.con.commit()
	    self.con.close()
	  return False
	else:
	  return True
      except KeyError:
	return True

    def on_error(self, status):
        print status
     
    def on_delete(self, status_id, user_id):
        self.delout.write( str(status_id) + "\n")
        return

    def on_limit(self, track):
        sys.stderr.write(track + "\n")
        return

    def on_error(self, status_code):
        sys.stderr.write('Error: ' + str(status_code) + "\n")
        return False

    def on_timeout(self):
        sys.stderr.write("Timeout, sleeping for 60 seconds...\n")
        time.sleep(60)
        return 
        
    def write_to_db(self, data,rt_stat, is_response):
      post_rt=json.loads(data)['retweeted']
      post_id=json.loads(data)['id']
      post_text=json.loads(data)['text']
      post_text=re.sub(r'\W\s', '', post_text)
      #post_text=re.sub(r'(?<!\w)@\w+', '', post_text)
      print self.tweet_count
      print post_text
      post_creat_time=json.loads(data)['created_at']
      self.tweet_count+=1
      
      #--------------- WRITING TO DATABASE

      try: 
	  
	  tweet=[(self.tweet_count, post_id, post_text, post_rt, rt_stat, is_response, post_creat_time)]
	  
	  query = "INSERT INTO tweets VALUES (?, ?, ?, ?, ?, ? ,?)"
	  self.cur.executemany(query, tweet)
	  

      except lite.Error, e:
	  
	  if self.con:
	      self.con.rollback()
	  
	  print 'Error %s' % e    
	  sys.exit(1)
#=======================================================================


#Open & create database
con = None

try:
     
    con = lite.connect(database='tweets.db') 
  
    cur = con.cursor()  
    
    cur.execute("DROP TABLE IF EXISTS tweets")
    query="CREATE TABLE tweets(\
    our_id INT PRIMARY KEY,\
    tweet_id INT,\
    body TEXT,\
    retweeted BOOLEAN,\
    retweeted_status BOOLEAN,\
    is_reply BOOLEAN,\
    created DATE)"
    cur.execute(query)
        
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

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
twitterStream = Stream(auth, listener())

twitterStream.filter(track=['and'],languages=['en'])
#languages filter doesn't work with out a tracking
#filter, so we add a bogus one.