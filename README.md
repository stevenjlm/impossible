# Impossible Hackathon: Project Aaki's Rankings

Proof of concept code for streaming, storing, and ranking wishes on www.impossible.com. Content management on the website can use the rankings to help users post and search for wishes.

## Illustration

Imagine farmer Kevin in vegiville. Kevin uses impossible.com to share carrots from his garden with locals. Vegiville residents, however, read articles online that encourage eating more beats. They are posting to the website, but their wishes for beats are going unfulfilled.

Now imagine Teresa, a new vegiville resident. Teresa wants to start her own home garden, but doesn't know what to grow. Thanks to the rankings features on impossible.com she is able to search wishes that are going unfulfilled to identify local residents needs. Clearly, people want more beats.

Teresa starts growing beats in her garden while giving some to local residents. Vegiville residents are happier and the world is a better place!

## Progress Report

This program does not yet use data from impossible.com. The hackathon API does not provide enough data to perform meaningful statistics. For now, we use twitter data to test machine learning algorithms.

The program currently streams live data from Twitter. We then train the program to recognize the language features that differentiate tweet replies from original tweets. This is analagous to finding the language features that differentiate wishes that have been fulfuled versus wishes that have gone ignored.

## Project Setup

To run the program you must first install the correct python modules listed in the "requirements.txt" file. You will need internet access, but only through http, and https protocols.

To collect data, go to the "twitter_api" directory and type

```bash
~/twitter/api$python stream.py
```
in the shell.

To analyse data, place the "twitter.db" file in the analyse directory. Run the following command,

```bash
~/analyse/api$python analyse.py
```

## Works in Progress

### New Algorithms

Word trees, maximum entropy, SVM.

### Optimizations

# License

Copyright 2014 Steven Munn, Maxime Egorov. All rights reserved. Contact authors for permissions.