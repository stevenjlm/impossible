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
tweet_set = []     # will be a list of tuples
all_text=''        # String with all text data from twitter
total_count=0      # Number of tweets
reply_count=0      # Number of tweets that are replies
new_count=0        # ------- that are original
maximum=2000       # Maximum number of tweets

try:
     
    con = lite.connect(database='tweets_r.db') 
  
    cur = con.cursor()
    cur.execute("SELECT * FROM tweets")

    while total_count<(maximum+1):
      
        data = cur.fetchone()
        
        if data == None:
            break
	
	text_row=filter_text(data[2])
	
	#use [4] for retweets rather than replies
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
word_features = all_words.keys()[:3]

def document_features(document):
  document_words = set(document)
  features = {}
  for word in word_features:
      features['contains(%s)' % word] = (word in document_words)
  return features

featuresets = [(document_features(d), c) for (d,c) in tweet_set]
train_set, test_set = featuresets[1000:], featuresets[:1000]
classifier = nltk.NaiveBayesClassifier.train(train_set)

#print '--'
#print classifier._feature_probdist.items()
#print '--'

#for label in self._labels:
            #for (fname, fval) in featureset.items():
                #if (label, fname) in self._feature_probdist:
                    #feature_probs = self._feature_probdist[label,fname]
                    #print fname
                    #print feature_probs.logprob(fval)
                    #logprob[label] += feature_probs.logprob(fval)
                #else:
                    ## nb: This case will never come up if the
                    ## classifier was created by
                    ## NaiveBayesClassifier.train().
                    #logprob[label] += sum_logs([]) # = -INF.

  
#features = set()
#for (label, fname), probdist in classifier._feature_probdist.items():
  #for fval in probdist.samples():
      #feature = (fname, fval)
      #features.add( feature )
      #p = probdist.logprob(fval)
      #print feature
      #print p
      
features = set()
for (label, fname), probdist in classifier._feature_probdist.items():
  for fval in probdist.samples():
      feature_probs = classifier._feature_probdist[label,fname]
      print fname
      print feature_probs.logprob(fval)

print '------DIFF'

test='I am answering this'
tokens = nltk.word_tokenize(test)
feat=document_features(tokens)
probadict=classifier.prob_classify(feat)
for samples in probadict.samples():
  print samples
  print probadict.prob(samples)

#classifier.show_most_informative_features(10)