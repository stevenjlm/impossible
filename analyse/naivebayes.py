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
from nltk.stem.lancaster import LancasterStemmer

import sqlite3 as lite

import random
import math

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
document_set = []     # will be a list of tuples
all_text=''        # String with all text data from twitter
total_count=0      # Number of tweets
reply_count=0      # Number of tweets that are replies
new_count=0        # ------- that are original
maximum=2000       # Maximum number of tweets

try:
     
    st = LancasterStemmer()
    con = lite.connect(database='tweets_r.db') 
  
    cur = con.cursor()
    cur.execute("SELECT * FROM tweets")
    update_tuple=[]

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
	    document_set.append((list(tokens), True))
	    reply_count+=1
	  else:
	    pass
	else:
	  #Isn't a reply
	  if new_count<(maximum/2+1):
	    raw_text=text_row
	    all_text+=text_row
	    tokens = nltk.word_tokenize(raw_text)
	    words=[st.stem(i) for i in list(tokens)]
	    document_set.append((words, False))
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
      
whole_set=document_set

document_set=whole_set[0:1000]
test_set=whole_set[1000:2000]

random.shuffle(document_set)

all_words = nltk.FreqDist(word.lower() for word in nltk.word_tokenize(all_text))

#Train Bernoulli Naive Bayes Classifier
#Notation inspired from http://nlp.stanford.edu/IR-book/html/htmledition/the-bernoulli-model-1.html
vocabulary=all_words.keys()[:1000]
N=len(document_set)

Nc_true=0
Nct_true={}
Nc_false=0
Nct_false={}

#initializes condprops,
for word in vocabulary:
      Nct_true[word]=0
      Nct_false[word]=0

for document in document_set:
  if document[1]==True:
    Nc_true+=1
    for word in vocabulary:
      if word in document[0]:
	Nct_true[word]+=1
  else:
    Nc_false+=1
    for word in vocabulary:
      if word in document[0]:
	Nct_false[word]+=1
    

prior={}
prior[0]=Nc_false/N
prior[1]=Nc_true/N
condpropF={}
condpropT={}
for word in vocabulary:
      condpropT[word]=(Nct_true[word]+1)/(Nc_true+2)
      condpropF[word]=(Nct_false[word]+1)/(Nc_false+2)


def apply_model(test_set,prior,condpropF,condpropT,vocabulary):
  success=0
  failures=0
  for test in test_set:
    score_true=math.log(prior[1])
    score_false=math.log(prior[0])
    test_words=test[0]
    for word in vocabulary:
      if word in list(set(test_words)):
	score_true+=math.log(condpropT[word])
	score_false+=math.log(condpropF[word])
      else:
	score_true+=math.log(1-condpropT[word])
	score_false+=math.log(1-condpropF[word])
    
    if score_true > score_false:
      guess=True
    else:
      guess=False
    
    if guess==test[1]:
      success+=1
    else:
      failures+=1
  
  print success/(failures+success)*100
  
apply_model(test_set,prior,condpropF,condpropT,vocabulary)












#def document_features(document):
  #document_words = set(document)
  #features = {}
  #for word in word_features:
      #features['contains(%s)' % word] = (word in document_words)
  #return features

#featuresets = [(document_features(d), c) for (d,c) in document_set]
#train_set, test_set = featuresets[1000:], featuresets[:1000]
#classifier = nltk.NaiveBayesClassifier.train(train_set)