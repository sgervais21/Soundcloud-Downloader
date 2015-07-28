#!/usr/bin/python

import sys, requests, os, re, json, webbrowser


#TODO: Get URL from command line, confirm it is soundcloud URL
if len(sys.argv) == 1:
    print "Need a valid Soundcloud URL"
    sys.exit()

urlregex = re.compile(r'^https://soundcloud.com/.*/.*')
urlmo = urlregex.search(sys.argv[1])
if urlmo == None:
    print 'No regex found'
    sys.exit()

url = 'http://api.soundcloud.com/resolve?url=' + urlmo.group(0) + '&client_id=YOUR_CLIENT_ID'

print url
#TODO: Get access to JSON from URL
try: 
    res = requests.get(url)
    res.raise_for_status()
except:
    print "Not valid Soundcloud URL"
    sys.exit()
jsd = json.loads(res.text)



streamurl = 'https://api.soundcloud.com/tracks/' + str(jsd['id']) + '/stream?client_id=YOUR_CLIENT_ID'

print streamurl
#Test if we can get stream from track URL
webbrowser.open(streamurl)
#TODO: Get track name/artist info from JSON file

#TODO: Create file and download track to that file

