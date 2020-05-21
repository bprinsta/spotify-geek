import spotipy
import json

from flask import render_template, url_for, request
from app import app
from app.track import Track
from spotipy.oauth2 import SpotifyClientCredentials
from datetime import datetime

track_uri = {}
track_uri['tyler'] = 'spotify:track:5hVghJ4KaYES3BFUATCYn0'
track_uri['joey'] = 'spotify:track:0O5brqyThK4RkcbhGGwJZU'
track_uri['lazlo'] = 'spotify:track:6eiP01Xsp3n9opK1Ucq5UB'
track_uri['harry'] = 'spotify:track:73hAYcA5TznG8rtuX1k9Ka'
track_uri['butter'] = 'spotify:track:6iCJCZqDJjmBxt07Oid6FI'
track_uri['pigs'] = 'spotify:track:59FwEQpuagQZQVP71h9OIq'

spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

pitch_class_notation = {0:'C', 1:'C♯', 2:'D', 3:'E♭', 4:'E', 5:'F', 6:'F♯', 7:'G', 8:'A♭', 9:'A', 10:'B♭', 11:'B'}

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    track_req = spotify.track(track_uri['lazlo'])
    analysis_req = spotify.audio_analysis(track_uri['lazlo'])
    features_req = spotify.audio_features(tracks=[track_uri['lazlo']])[0]

    # Track Basic Info
    track = {}
    track['uri'] = track_uri['lazlo']
    track['name'] = track_req['name']

    track['album'] = track_req['album']['name']
    track['album_art'] = track_req['album']['images'][0]
    release_datetime_object = datetime.strptime(track_req['album']['release_date'], '%Y-%m-%d')
    track['release_date'] = release_datetime_object.strftime('%Y')
    
    track['artists'] = []
    for artist in track_req['artists']:
        track['artists'].append(artist['name'])

    features = {}
    features['duration_ms'] = datetime.fromtimestamp(features_req['duration_ms'] / 1000).strftime('%-M:%S')
    features['key'] = pitch_class_notation[features_req['key']]
    features['mode'] =  'Minor' if features_req['mode'] == 0 else 'Major'
    features['time_signature'] = features_req['time_signature']
    features['tempo'] = round(features_req['tempo'])
    features['bars'] = len(analysis_req['bars'])
    
    features['acousticness'] = features_req['acousticness']
    features['danceability'] = features_req['danceability']
    features['energy'] = features_req['energy']
    features['instrumentalness'] = features_req['instrumentalness']
    features['liveness'] = features_req['liveness']
    features['speechiness'] = features_req['speechiness']
    features['valence'] = features_req['valence']
    

    return render_template('track.html', track=track, features=features)

@app.route("/search", methods=['POST'])
def search():
    q = request.form.get('q')
    search_results = spotify.search(q=q, limit=20, type='track')
    
    tracks = []
    # print(search_results)
    # print(search_results['tracks']['items'])
    for result in search_results['tracks']['items']:
        track = {}
        track['name'] = result['name']
        track['album'] = result['album']['name']
        track['album_art'] = result['album']['images'][0]

        track['artists'] = []
        for artist in result['artists']:
            track['artists'].append(artist['name'])

        track['uri'] = result['uri']
        tracks.append(track)
        # print(track['name'])
        # print(track['album']['name'])

    return render_template('search.html', query=q, tracks=tracks)

@app.errorhandler(404)
def error_404(error):
    return render_template('error.html'), 404
