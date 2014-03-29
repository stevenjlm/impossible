from __future__ import division
import nltk, re, pprint
from optparse import OptionParser

import sqlite3 as lite

import random

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
raw_text=''
tokens = nltk.word_tokenize(raw_text)
tweet_set = [] #will be a list of tuples
all_text=''
total_count=0
reply_count=0
new_count=0
maximum=2000

try:
     
    con = lite.connect(database='tweets_r.db') 
  
    cur = con.cursor()
    cur.execute("SELECT * FROM tweets")
    update_tuple=[]

    while total_count<(maximum+1):
      
        data = cur.fetchone()
        
        if data == None:
            break
	
	text_row=filter_text(data[2])
	
	#use [4] for retweets
	if data[5] == 1:
	  #Is a reply
	  if reply_count<(maximum/2+1):
	    raw_text=text_row
	    all_text+=text_row
	    tokens = nltk.word_tokenize(raw_text)
	    tweet_set.append((list(tokens), True))
	    reply_count+=1
	  else:
	    pass
	else:
	  #Isn't a reply
	  if new_count<(maximum/2+1):
	    raw_text=text_row
	    all_text+=text_row
	    tokens = nltk.word_tokenize(raw_text)
	    tweet_set.append((list(tokens), False))
	    new_count+=1
	  else:
	    pass
	  
	total_count=reply_count+new_count

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
word_features = all_words.keys()[:2000]

def document_features(document):
  document_words = set(document)
  features = {}
  for word in word_features:
      features['contains(%s)' % word] = (word in document_words)
  return features

featuresets = [(document_features(d), c) for (d,c) in tweet_set]
train_set, test_set = featuresets[1000:], featuresets[:1000]
classifier = nltk.NaiveBayesClassifier.train(train_set)

print nltk.classify.accuracy(classifier, test_set)

classifier.show_most_informative_features(10)
#raw_text="Yo dawg, you're totally right! I'm so derp"
raw_text="Attention, I will now be eating breakfeast at 10am now"
tokens = nltk.word_tokenize(raw_text)
#tweet_test=[]
#tweet_test.append(list(tokens))
featuretest = document_features(tokens)

dist = classifier.prob_classify(featuretest)
for label in dist.samples():
    print("%s: %f" % (label, dist.prob(label)))
    
raw_text="Yo dawg, you're totally right! I'm so derp"
tokens = nltk.word_tokenize(raw_text)
#tweet_test=[]
#tweet_test.append(list(tokens))
featuretest = document_features(tokens)

dist = classifier.prob_classify(featuretest)
for label in dist.samples():
    print("%s: %f" % (label, dist.prob(label)))