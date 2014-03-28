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
  pass

#Connect to twitter
is_global=0;

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
api = tweepy.API(auth)


#Open database
con = None

try:
     
    con = lite.connect(database='tweets.db') 
  
    cur = con.cursor()
    cur.execute("SELECT * FROM tweets")

    while True:
      
        row = cur.fetchone()
        
        if row == None:
            break
            
        print row[1]
        data=api.get_status(row[1])
        
        print data.retweeted
        
    
    #cur.execute("DROP TABLE IF EXISTS tweets")
    #cur.execute("CREATE TABLE tweets(our_id INT PRIMARY KEY, tweet_id INT, body TEXT, retweet BOOLEAN, created DATE)")
    ##query = "INSERT INTO cars (id, name, price) VALUES (%s, %s, %s)"
    #cur.executemany(query, cars)
        
    #con.commit()
    

except lite.Error, e:
    
    if con:
        con.rollback()
    
    print 'Error %s' % e    
    sys.exit(1)
    
    
finally:
    
    if con:
        con.close()