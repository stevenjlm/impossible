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
import operator

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

document_set=[]
st = LancasterStemmer()

from nltk.corpus import movie_reviews
for category in movie_reviews.categories():
  if category=='pos':
      cat=True
  else:
      cat=False
      
  for fileid in movie_reviews.fileids(category):
    raw_text = movie_reviews.raw(fileid)
    raw_text = filter_text(raw_text)
    tokens = nltk.word_tokenize(raw_text)
    #words=[st.stem(i) for i in list(tokens)]
    document_set.append((list(tokens), cat))

random.shuffle(document_set)


test_set=document_set[0:600]

whole_set=document_set

document_set=whole_set[0:1400]

all_words = nltk.FreqDist(w.lower() for w in movie_reviews.words())

#Train Bernoulli Naive Bayes Classifier
#Notation inspired from http://nlp.stanford.edu/IR-book/html/htmledition/the-bernoulli-model-1.html
vocabulary=all_words.keys()[:2000]
N=len(document_set)

Nc_true=0
Nwords_ctrue=0
Nct_true={}
Nc_false=0
Nwords_cfalse=0
Nct_false={}

#initializes condprops,
for word in vocabulary:
      Nct_true[word]=0
      Nct_false[word]=0

for document in document_set:
  if document[1]==True:
    Nc_true+=1
    for word in vocabulary:
      Nct_true[word]+=document[0].count(word)
      Nwords_ctrue+=len(document[0])
  else:
    Nc_false+=1
    for word in vocabulary:
      Nct_false[word]+=document[0].count(word)
      Nwords_cfalse+=len(document[0])
    

prior={}
prior[0]=Nc_false/N
prior[1]=Nc_true/N
print prior
condpropF={}
condpropT={}
for word in vocabulary:
      condpropT[word]=(Nct_true[word]+1)/(Nwords_ctrue+len(vocabulary))
      condpropF[word]=(Nct_false[word]+1)/(Nwords_cfalse+len(vocabulary))


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
    
    if score_true > score_false:
      guess=True
    else:
      guess=False
    
    if guess==test[1]:
      success+=1
    else:
      failures+=1
  
  print success/(failures+success)*100
  #print sorted(condpropT.iteritems(), key=operator.itemgetter(1))
  
apply_model(test_set,prior,condpropF,condpropT,vocabulary)

def write_to_file(condpropT,condpropF,prior,vocabulary):
  #Prior
  f=open('to_db_nltk.txt','w')
  f.write('CREATE TABLE vocabulary (word TEXT, condpropT DOUBLE, condpropF DOUBLE);\n')
  f.write('INSERT INTO vocabulary VALUES ("prior", ' + str(prior[1]) +' , ' + str(prior[0]) + ');\n')
  for word in vocabulary:
    query='INSERT INTO vocabulary VALUES ("' + word + '", ' + str(condpropT[word]) +' , ' + str(condpropF[word]) + ');\n'
    f.write(query)

write_to_file(condpropT,condpropF,prior,vocabulary)






#def document_features(document):
  #document_words = set(document)
  #features = {}
  #for word in word_features:
      #features['contains(%s)' % word] = (word in document_words)
  #return features

#featuresets = [(document_features(d), c) for (d,c) in document_set]
#train_set, test_set = featuresets[1000:], featuresets[:1000]
#classifier = nltk.NaiveBayesClassifier.train(train_set)