#!/usr/bin/python

import sys, requests, os, re, json, webbrowser, time

def strToFile(name):
    toretr = '_'.join(name.split(' '))
    #Fix annoying common naming convention (ex. artist_name_-_track_name)
    toretr = re.sub(r'/', '-', toretr)
    return re.sub(r'_-_', '-', toretr)

def fileSize(bytes):
    if bytes < 1000:
        return str(bytes) + " bytes"
    elif bytes < 1000 ** 2:
        return "{:.1f} kB".format(bytes/1000.0)
    elif bytes < 1000 ** 3:
        return "{:.1f} MB".format(bytes/1000000.0)


def downloadTrack(id_num):
    try:
        res = requests.get('http://api.soundcloud.com/tracks/' + str(id_num) + '?client_id=YOUR_CLIENT_ID')
        res.raise_for_status()
    except:
        print 'Not a valid URL'
        sys.exit()
    
    
    jsobj = json.loads(res.text)
    if jsobj["streamable"] == False:
        print "\nCould not download " + jsobj['title'] + " because it isn't streamable :(\n"
        return
    streamurl = 'https://api.soundcloud.com/tracks/' + str(jsobj['id']) + '/stream?client_id=YOUR_CLIENT_ID'

#TODO: Get track name/artist info from JSON file, prepare info for new file
    trackname = jsobj['title']
    artist = jsobj['user']['username']
    approx_bytes = (jsobj['duration'] / 1000) * 16000 #approximation at 128 kbps

    filename = strToFile(trackname)
    dirname = strToFile(artist)
    size = fileSize(approx_bytes)
    #TODO: Create file and download track to that file
    if dirname not in os.listdir(os.getcwd()):
        os.makedirs(os.path.join(os.getcwd(), dirname))
    try:
        streamres = requests.get(streamurl, stream=True)
        streamres.raise_for_status()
        length = streamres.headers.get('content-length')
    except:
        print "Could not connect to stream"
        sys.exit()

    if (filename + '.mp3') not in os.listdir(os.path.join(os.getcwd(), dirname)):
        f = open(os.path.join(os.getcwd(), dirname, filename) + '.mp3', 'wb')
        print '\n' + "Now Downloading"
        print "Track: " + trackname
        print "Artist: " + artist
        print "Size: " + size
        dl = 0
        length = float(length)
        for chunk in streamres.iter_content(10000):
            dl += len(chunk)
            f.write(chunk)
            sys.stdout.write("\r{:.1%} Downloaded".format(dl/length))
            sys.stdout.flush()
        f.close()
        sys.stdout.write('\n\n')
        print "Download of " + trackname + " complete!"
        sys.stdout.write('\n')
    else:
        print '\n' + filename + '.mp3 already exists!'

#TODO: Get URL from command line, confirm it is soundcloud URL

def downloadFavorites(username, id_num):
    fav_url = 'https://api.soundcloud.com/users/' + str(id_num) + '/favorites?client_id=YOUR_CLIENT_ID'
    try:
        res = requests.get(fav_url)
        res.raise_for_status()
    except:
        print "Not valid user favorites playlist"
        sys.exit()
    jsobj = json.loads(res.text)
    for i in jsobj:
        downloadTrack(i['id'])


if len(sys.argv) == 1:
    print "Usage: ./sc.py <Soundcloud URL>"
    print "       or"
    print "       ./sc.py <username>"
    sys.exit()

playlist_regex = re.compile(r'^http(s)?://soundcloud.com/.*/sets/.*')
urlregex = re.compile('^http(s)?://soundcloud.com/.*/.*')
playlistmo = playlist_regex.search(sys.argv[1])
if playlistmo == None:
    urlmo = urlregex.search(sys.argv[1])
    if urlmo == None:
        username = sys.argv[1]
        url = 'http://api.soundcloud.com/resolve?url=https://soundcloud.com/'               + username + '&client_id=YOUR_CLIENT_ID'
        playlist = False
        user = True
    else:
        url = 'http://api.soundcloud.com/resolve?url=' + urlmo.group(0) +              '&client_id=YOUR_CLIENT_ID'
        playlist = False
        user = False
else:
    url = 'http://api.soundcloud.com/resolve?url=' + playlistmo.group(0) +                      '&client_id=YOUR_CLIENT_ID'
    playlist = True
    user = False
#TODO: Get access to JSON from URL

try: 
    res = requests.get(url)
    res.raise_for_status()
except:
    print "Not a valid URL"
    sys.exit()

jsd = json.loads(res.text)
if user == True:
    print "Downloading " + username + "'s favorites!"
    dirname = strToFile(username) + '_' + 'favorites'
    if dirname not in os.listdir(os.getcwd()):
        os.makedirs(os.path.join(os.getcwd(), dirname))
    os.chdir(os.path.join(os.getcwd(), dirname))
    downloadFavorites(username, jsd['id'])

elif playlist == False:
    downloadTrack(jsd['id'])

else:
    tracklist = jsd['tracks']
    for i in tracklist:
        downloadTrack(i['id'])
