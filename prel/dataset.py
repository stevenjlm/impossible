#general libraries
from __future__ import division
#MySQLtext, and MySQLThanks
import MySQLdb as mdb
import sys
#MySQLtext
import nltk
#filter_text
import re, pprint

class dataset:
  
  def talk(self,to_print):
    if self.verbose==1:
      print to_print
  
  def filter_text(self,raw_text):
    raw_text=raw_text.lower()
    raw_text=re.sub(r'\W\s', '', raw_text)
    raw_text=re.sub(r'(?<!\w)@\w+', '', raw_text)
    raw_text=re.sub('[^\x00-\x7F]+', ' ', raw_text)
    raw_text=re.sub('rt', '', raw_text)
    raw_text=re.sub('#', ' ', raw_text)
    raw_text=re.sub('^https?:\/\/.*[\r\n]*', ' ', raw_text)
    return raw_text
  
  def MySQLtext(self,max_count):
    
    #Open database
    self.wish_set = []
    self.all_text=''
    self.total_count=0
    self.thanked_count=0
    self.unthanked_count=0
    self.maximum=max_count
    iRow=0
    self.talk("Retrieving wishes from database")
    try:
	con = mdb.connect('localhost','fred','freddy','impossible_dump') 
      
	cur = con.cursor()
	cur.execute("SELECT Title, ReceivedThanks FROM Wish;")
	all_data = cur.fetchall()
	while self.total_count<(self.maximum+1):
      
	  data=all_data[iRow]
	  
	  if data == None:
	    break
	  
	  if data[1] == 1:
	    #Is thanked
	    if self.thanked_count<(self.maximum/2+1):
	      #text_row=self.filter_text(data[0])
	      text_row=data[0]
	      self.all_text+=text_row
	      tokens = nltk.word_tokenize(text_row)
	      self.wish_set.append((list(tokens), True))
	      self.thanked_count+=1
	    else:
	      pass
	  else:
	    #Isn't a reply
	    if self.unthanked_count<(self.maximum/2+1):
	      text_row=self.filter_text(data[0])
	      self.all_text+=text_row
	      tokens = nltk.word_tokenize(text_row)
	      self.wish_set.append((list(tokens), False))
	      self.unthanked_count+=1
	    else:
	      pass
	    
	  self.total_count=self.thanked_count+self.unthanked_count
	  iRow+=1

    except mdb.Error, e:
      
	print "Error %d: %s" % (e.args[0],e.args[1])
	sys.exit(1)
	
    finally:
	    
	if con:    
	    con.close()
	self.talk("Gathered data with no errors")
	return None
  
  def MySQLThanks(self):
    
    try:
	con = mdb.connect('localhost','fred','freddy','impossible_dump') 
      
	cur = con.cursor()
	cur.execute("SELECT ReceivedThanks FROM Wish")
	
	rows = cur.fetchall()

	for row in rows:
	  self.total+=1
	  if row[0]:
	    self.thanked+=1

	print "Number of wishes Thanked, "
	print self.thanked
	print "Total number wishes"
	print self.total
	print "Ratio"
	print (self.thanked/self.total)*100

	
    except mdb.Error, e:
      
	print "Error %d: %s" % (e.args[0],e.args[1])
	sys.exit(1)
	
    finally:    
	    
	if con:    
	    con.close()
	return None
  
  def __init__(self):
    self.total=0
    self.thanked=0
    self.verbose=1
    return None