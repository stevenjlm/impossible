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

content=['cats','dogs']

with open('nouns.txt') as f:
    words = f.readlines()
   
raw_text=''
tweet_set = []
all_text=''

for _ in range(0,3000):
  noun=content[random.randint(0,1)]
  if noun=='cats':
    thanks=True
  else:
    thanks=False
  raw_text= noun
  tokens = nltk.word_tokenize(raw_text)
  tweet_set.append((list(tokens), thanks))
  all_text+= ' ' + raw_text
  
print tweet_set

random.shuffle(tweet_set)

all_words = nltk.FreqDist(word.lower() for word in nltk.word_tokenize(all_text))
word_features = all_words.keys()[:2]

print word_features

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