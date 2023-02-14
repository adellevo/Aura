import os
from flask import Flask, redirect, render_template
from app import app
import urllib
from urllib.parse import quote 

#  Client Keys
CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")

# Spotify URLS
SPOTIFY_AUTH_URL = os.environ.get("SPOTIFY_AUTH_URL")
SPOTIFY_TOKEN_URL = os.environ.get("SPOTIFY_TOKEN_URL")
SPOTIFY_API_BASE_URL = os.environ.get("SPOTIFY_API_BASE_URL")
API_VERSION = os.environ.get("API_VERSION")
SPOTIFY_API_URL = "{}/{}".format(SPOTIFY_API_BASE_URL, API_VERSION)

# Server-side Parameters
CLIENT_SIDE_URL = os.environ.get("CLIENT_SIDE_URL")
REDIRECT_URI = os.environ.get("REDIRECT_URI")
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