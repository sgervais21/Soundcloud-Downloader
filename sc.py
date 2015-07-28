#!/usr/bin/python

import sys, requests, os, re, json, webbrowser


#TODO: Get URL from command line, confirm it is soundcloud URL
if len(sys.argv) == 1:
    print "Usage: ./sc.py <Soundcloud URL>"
    sys.exit()
urlregex = re.compile(r'^https://soundcloud.com/.*/.*')
urlmo = urlregex.search(sys.argv[1])
if urlmo == None:
    print 'Not a valid SoundCloud Track URL'
    sys.exit()
url = 'http://api.soundcloud.com/resolve?url=' + urlmo.group(0) + '&client_id=YOUR_CLIENT_ID'

#TODO: Get access to JSON from URL
try: 
    res = requests.get(url)
    res.raise_for_status()
except:
    print "Not a valid URL"
    sys.exit()
jsd = json.loads(res.text)
streamurl = 'https://api.soundcloud.com/tracks/' + str(jsd['id']) + '/stream?client_id=YOUR_CLIENT_ID'

#TODO: Get track name/artist info from JSON file, prepare info for new file

trackname = jsd['title']
artist = jsd['user']['username']
print trackname
print artist

filename = '_'.join(trackname.split(' '))
dirname = '_'.join(trackname.split(' '))

#Annoying Look for filename with single dash
weirdDash = re.compile(r'_-_')



#TODO: Create file and download track to that file

