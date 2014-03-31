#
#		Project AAKI's Rankings
#		Testing Streamer
#			Gathers test data from Twitter
#			Saves it to SQLite3 database
#
#	Steven and Max
#		https://github.com/stevenjlm/impossible
#		License in README.markdown

# ======================= THIS CODE WAS ABANDONED ==================
# See other files in directory
# ==================================================================

from __future__ import division
import nltk, re, pprint

import sqlite3 as lite

import random
import nltk

#Filtering function for raw text
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
raw_text=''
tokens = nltk.word_tokenize(raw_text)
tweet_set = [] #will be a list of tuples
all_text=''

try:
     
    con = lite.connect(database='tweets.db') 
  
    cur = con.cursor()
    cur.execute("SELECT * FROM tweets WHERE our_id<10")
    update_tuple=[]

    while True:
      
        data = cur.fetchone()
        
        if data == None:
            break
	
	text_row=filter_text(data[2])
	
	if data[4] == 1:
	  raw_text=text_row
	  all_text+=text_row
	  tokens = nltk.word_tokenize(raw_text)
	  tweet_set.append((list(tokens), False))
	  print list(tokens)
	else:
	  raw_text=text_row
	  all_text+=text_row
	  tokens = nltk.word_tokenize(raw_text)
	  tweet_set.append((list(tokens), True))
	  print list(tokens)

except lite.Error, e:
    
    if con:
        con.rollback()
    
    print 'Error %s' % e    
    sys.exit(1)
    
    
finally:
    
    if con:
        con.close()
        

random.shuffle(tweet_set)

all_words = nltk.FreqDist(word.lower() for word in nltk.word_tokenize(all_text))
word_features = all_words.keys()[:3]

def document_features(document):
  document_words = set(document)
  features = {}
  for word in word_features:
      features['contains(%s)' % word] = (word in document_words)
  return features

featuresets = [(document_features(d), c) for (d,c) in tweet_set]
train_set, test_set = featuresets[4:], featuresets[:4]
classifier = nltk.NaiveBayesClassifier.train(train_set)

print nltk.classify.accuracy(classifier, test_set)

classifier.show_most_informative_features(1)