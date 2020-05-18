import os
from flask import Flask

app = Flask(__name__)
app.config['SPOTIPY_CLIENT_ID'] = os.environ.get('SPOTIPY_CLIENT_ID')
app.config['SPOTIPY_CLIENT_SECRET'] = os.environ.get('SPOTIPY_CLIENT_SECRET')
    
from app import routes