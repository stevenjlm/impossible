#
#		Project AAKI's Rankings
#		Testing Streamer
#			Gathers test data from Twitter
#			Saves it to SQLite3 database
#
#	Steven and Max
#		https://github.com/stevenjlm/impossible
#		License in README.markdown

# IMPORTANT: This script will not work with
# the standard tweepy files. Check the
# ../tweepy-mods directory for the replacement
# scripts.

import httplib, urllib
import json

# Get all the id's
params = urllib.urlencode({'@ID': 'LN011ZmTVc74cSsXAJsmKPjb4oyfb5Yy', 'LocalsFilter' : 2})
headers = {"Content-Type": "json", "Content-Length": str(len(params))}
conn = httplib.HTTPConnection("eae.no-ip.biz")
conn.request("POST", "/hackathon/api_hackathon/home/getHomeStreamIDs", params, headers)
response = conn.getresponse()
print response.status, response.reason
data = response.read()
print data
json_obj=json.loads(data)

# Compile list into the appropreate string format
IDs=''
for i in range(0,len(json_obj)):
  IDs+=json_obj[i]['ID']
  if i<(len(json_obj)-1):
    IDs+=','
  else:
    IDs+=''
  

# get all the whishes for the retrieved IDs,
params = urllib.urlencode({'IDs':IDs})
conn = httplib.HTTPConnection("eae.no-ip.biz")
conn.request("POST", "/hackathon/api_v2/home/GetHomeData/", params)
response = conn.getresponse()
print response.status, response.reason
data = response.read()
print data

# ==TODO===
'''
Extract wishes and thank you's for wishes
Save them to SQLite3 database
'''