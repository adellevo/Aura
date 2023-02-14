from flask import Flask, redirect, render_template
from app import app
import urllib
from urllib.parse import quote 

import os
from dotenv import load_dotenv

load_dotenv()

#  Client Keys
CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")

# Spotify URLS
SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_API_BASE_URL = "https://api.spotify.com"
API_VERSION = "v1"
SPOTIFY_API_URL = "{}/{}".format(SPOTIFY_API_BASE_URL, API_VERSION)

# Server-side Parameters
CLIENT_SIDE_URL = "http://localhost:5000/"
REDIRECT_URI = "http://localhost:5000/dashboard"
SCOPE = 'user-read-private user-read-playback-state user-modify-playback-state user-library-read'
STATE = ""
SHOW_DIALOG_bool = True
SHOW_DIALOG_str = str(SHOW_DIALOG_bool).lower()

auth_query_parameters = {
    "response_type": "code",
    "redirect_uri": REDIRECT_URI,
    "scope": SCOPE,
    "client_id": CLIENT_ID
}

@app.route('/login')
def spotify():
    return render_template('login.html')

@app.route('/spotify_authentication')
def spotify_auth():
    url_args = "&".join(["{}={}".format(key,urllib.parse.quote(val)) for key, val in auth_query_parameters.items()])
    auth_url = "{}/?{}".format(SPOTIFY_AUTH_URL, url_args)
    return redirect(auth_url)
 
@app.route('/dashboard')
def aura():
    return render_template('dashboard.html')