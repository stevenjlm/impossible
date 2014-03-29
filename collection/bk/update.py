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

#Connect to twitter

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
api = tweepy.API(auth)


#Open database
con = None

try:
     
    con = lite.connect(database='tweets10-4.db') 
  
    cur = con.cursor()
    cur.execute("SELECT * FROM tweets")
    update_tuple=[]

    while True:
      
        data = cur.fetchone()
        
        if data == None:
            break
        
        #3 attemps
        attempts=0
        try_again=True
        while try_again:
	  try:
	    new_rt=api.get_status(data[1])
	    update_tuple.append((new_rt.retweeted,data[0]))
	    print new_rt.retweeted
	  except tweepy.error.TweepError:
	    attempts+=1
	    if attempts > 2:
	      try_again=False
	      print("error")
	 
	attempts=0
        try_again=True
        
        
    
    query="UPDATE tweets SET retweet=? WHERE our_id=?"
    cur.executemany(query, update_tuple)
    con.commit()
    

except lite.Error, e:
    
    if con:
        con.rollback()
    
    print 'Error %s' % e    
    sys.exit(1)
    
    
finally:
    
    if con:
        con.close()