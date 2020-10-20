import tweepy
import csv
import pandas as pd
import sys
####input your credentials here
consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth,wait_on_rate_limit=True)
#####corona
# Open/Create a file to append data
csvFile = open('ua.csv', 'a')
#Use csv Writer
csvWriter = csv.writer(csvFile)

for tweet in tweepy.Cursor(api.search,q="#corona",count=100,
                           lang="en",
                           since="2017-04-03").items():
    print (tweet.created_at, tweet.text)
    csvWriter.writerow([tweet.created_at, tweet.text.encode('utf-8')])

if len(sys.argv) == 3:
    csvfile = open(sys.argv[1],'r')
    jsonfile = open(sys.argv[2], 'w')
elif len(sys.argv) == 2:
    csvfile = open(sys.argv[1],'r')
    jsonfile = open('retweets.json', 'w')
else:
    print "Usage - csvtojson.py inputfile.csv output.json"
    sys.exit()


arr=[]
headers = []

# Read in the headers/first row
for header in csvfile.readline().split(','):
    headers.append(header)

# Extract the information into the "xx" : "yy" format.
for line in csvfile.readlines():
  lineStr = ''
  for i,item in enumerate(line.split(',')):
      lineStr+='"'+headers[i] +'" : "' + item + '",\n'
  arr.append(lineStr)

csvfile.close()

#convert the array into a JSON string:
jsn = '{\n "data":['
jsnEnd = ']\n}'
for i in range(len(arr)-1):
    if i == len(arr)-2:
        jsn+="{"+str(arr[i])[:-2]+"}\n"
    else:
        jsn+="{"+str(arr[i])[:-2]+"},\n"
jsn+=jsnEnd

#write to file
jsonfile.write(jsn)
jsonfile.close()
print "Done."