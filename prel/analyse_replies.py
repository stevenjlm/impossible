#
#		Project AAKI's Rankings
#		Data Analyser
#			Reads test data from Twitter database
#			Creates Naive Bayes learning model
#
#	Steven and Max
#		https://github.com/stevenjlm/impossible
#		License in README.markdown

from __future__ import division
import nltk, re, pprint

import MySQLdb as mdb

import random
import sys

#FILTERS for raw text
def filter_text(raw_text):
  raw_text=raw_text.lower()
  raw_text=re.sub(r'\W\s', '', raw_text)
  raw_text=re.sub(r'(?<!\w)@\w+', '', raw_text)
  raw_text=re.sub('[^\x00-\x7F]+', ' ', raw_text)
  raw_text=re.sub('rt', '', raw_text)
  raw_text=re.sub('#', ' ', raw_text)
  raw_text=re.sub('^https?:\/\/.*[\r\n]*', ' ', raw_text)
  return raw_text



#Open database
con = None
total=0
thanked=0

try:
     
    con = mdb.connect('localhost','fred','freddy','impossible_dump') 
  
    cur = con.cursor()
    cur.execute("SELECT ReceivedThanks FROM Wish")
    
    rows = cur.fetchall()

    for row in rows:
      total+=1
      if row[0]:
	thanked+=1

    print "Number of wishes Thanked, "
    print thanked
    print "Total number wishes"
    print total
    print "Ratio"
    print thanked/total*100

    
except mdb.Error, e:
  
    print "Error %d: %s" % (e.args[0],e.args[1])
    sys.exit(1)
    
finally:    
        
    if con:    
        con.close()