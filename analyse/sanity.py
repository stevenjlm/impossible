from __future__ import division
from optparse import OptionParser

import sqlite3 as lite

#Open database

number_entries=0
number_replies=0

try:
     
    con = lite.connect(database='tweets_r.db') 
  
    cur = con.cursor()
    cur.execute("SELECT * FROM tweets")

    while True:
      
        data = cur.fetchone()
        
        if data == None:
            break
	
	number_entries+=1
	#use [4] for retweets
	if data[5] == 1:
	  number_replies+=1

except lite.Error, e:
    
    if con:
        con.rollback()
    
    print 'Error %s' % e    
    sys.exit(1)
    
    
finally:
    print number_replies/number_entries
    
    if con:
        con.close()