from flask import Flask, request, redirect, session, render_template, url_for
from jinja2 import Template
import json
import pylast
import random

app = Flask(__name__)

@app.route("/")
def index():
    print "someone connected"
    return render_template('index.html')

@app.route("/getartists",methods=['POST'])
def getartists():

    #pull the JSON out of the request
    jsonlist = []
    for key, value in request.form.iteritems():
        jsonlist.append(key)

    #if user tampered with the list or it was lost along the way
    if len(jsonlist) != 1:
        return "That's an odd number of JSON lists in your POST"

    #get the first (and only) JSON and parse the list
    artistsjson = jsonlist[0];
    artists = json.loads(artistsjson)

    #build the playlist from each artists' top songs
    playlist = []
    for artist in artists:
        for track in getTopTracks(artist):
            playlist.append(track)

    #randomize playlist
    random.shuffle(playlist)

    #convert the playlist to JSON and send it
    playlistdump = json.dumps(playlist)
    return playlistdump

#lastfm vars
api_key = 'YourLastFMApiKey'
api_secret = 'YourLastFMApiSecret'
network = pylast.LastFMNetwork(api_key,api_secret)

def getTopTracks(artist, count=3):
    global network
    artist = network.get_artist(artist)
    tracks = pylast.extract_items(artist.get_top_tracks())
    buildlist = []
    for track in tracks[:count]:
        buildlist.append([str(track.artist),str(track.title),str(track.get_duration())])
    return buildlist

if __name__ == "__main__":
    app.config['DEBUG'] = False
    app.run('0.0.0.0',80)