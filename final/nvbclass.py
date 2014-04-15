#general libraries
from __future__ import division

from dataset import dataset
import nltk, pprint

import random
import math
import operator

class nvbclass(dataset):
  
  def naive_bayes(self):
    whole_set=self.wish_set
    
    random.shuffle(whole_set)

    training_set=whole_set[0:1000]
    self.test_set=whole_set[1000:2000]

    self.talk("Extracting vocabulary")
    all_words = nltk.FreqDist(word.lower() for word in nltk.word_tokenize(self.all_text))

    #Train Bernoulli Naive Bayes Classifier
    #Notation inspired from http://nlp.stanford.edu/IR-book/html/htmledition/the-bernoulli-model-1.html
    self.vocabulary=all_words.keys()[:1000]
    print self.vocabulary
    N=len(training_set)
    
    self.talk("Initializing probability model")
    
    Nc_true=0
    Nwords_ctrue=0
    Nct_true={}
    Nc_false=0
    Nwords_cfalse=0
    Nct_false={}

    #initializes condprops,
    for word in self.vocabulary:
	  Nct_true[word]=0
	  Nct_false[word]=0
	  
    self.talk("Computing statistics for Naive Bayes model")
    for document in training_set:
      if document[1]==True:
	Nc_true+=1
	for word in self.vocabulary:
	  Nct_true[word]+=document[0].count(word)
	  Nwords_ctrue+=len(document[0])
      else:
	Nc_false+=1
	for word in self.vocabulary:
	  Nct_false[word]+=document[0].count(word)
	  Nwords_cfalse+=len(document[0])
	  
    self.talk("Building model from statistics")
    self.prior={}
    self.prior[0]=Nc_false/N
    self.prior[1]=Nc_true/N
    self.condpropF={}
    self.condpropT={}
    for word in self.vocabulary:
	  self.condpropT[word]=(Nct_true[word]+1)/(Nwords_ctrue+len(self.vocabulary))
	  self.condpropF[word]=(Nct_false[word]+1)/(Nwords_cfalse+len(self.vocabulary))

  def apply_model(self):
    self.talk("Applying model to new data set")
    self.success=0
    self.failures=0
    for test in self.test_set:
      score_true=math.log(self.prior[1])
      score_false=math.log(self.prior[0])
      test_words=test[0]
      for word in self.vocabulary:
	if word in list(set(test_words)):
	  score_true+=math.log(self.condpropT[word])
	  score_false+=math.log(self.condpropF[word])
      
      if score_true > score_false:
	guess=True
      else:
	guess=False
      
      if guess==test[1]:
	self.success+=1
      else:
	self.failures+=1
    print "Accuracy of,"
    
    print self.success/(self.failures+self.success)*100 , "%"
  
  def __init__(self):
    dataset.__init__(self)
    return None