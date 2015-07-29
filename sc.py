#!/usr/bin/python

import sys, requests, os, re, json, webbrowser, time

def strToFile(name):
    toretr = '_'.join(name.split(' '))
    #Fix annoying common naming convention (ex. artist_name_-_track_name)
    return re.sub(r'_-_', '-', toretr)

def fileSize(bytes):
    if bytes < 1000:
        return str(bytes) + " bytes"
    elif bytes < 1000 ** 2:
        return "{:.1f} kB".format(bytes/1000.0)
    elif bytes < 1000 ** 3:
        return "{:.1f} MB".format(bytes/1000000.0)


#TODO: Add functionality for playlists


#TODO: Get URL from command line, confirm it is soundcloud URL

if len(sys.argv) == 1:
    print "Usage: ./sc.py <Soundcloud URL>"
    sys.exit()

urlregex = re.compile(r'^https://soundcloud.com/.*/.*')

urlmo = urlregex.search(sys.argv[1])
if urlmo == None:
    print 'Not a valid SoundCloud Track URL'
    sys.exit()
url = 'http://api.soundcloud.com/resolve?url=' + urlmo.group(0) +                      '&client_id=YOUR_CLIENT_ID'

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
approx_bytes = (jsd['duration'] / 1000) * 16000 #approximation at 128 kbps

filename = strToFile(trackname)
dirname = strToFile(artist)
size = fileSize(approx_bytes)

#TODO: Create file and download track to that file

if dirname not in os.listdir(os.getcwd()):
    os.makedirs(os.path.join(os.getcwd(), dirname))
try:
    streamres = requests.get(streamurl)
    streamres.raise_for_status()
except:
    print "Could not connect to stream"
    sys.exit()

if (filename + '.mp3') not in os.listdir(os.path.join(os.getcwd(), dirname)):
    f = open(os.path.join(os.getcwd(), dirname, filename) + '.mp3', 'wb')
    print '\n' + "Now Downloading"
    print "Track: " + trackname
    print "Artist: " + artist
    print "Size: " + size
    count = 0.0
    for chunk in streamres.iter_content(1000):
        f.write(chunk)
    f.close()
