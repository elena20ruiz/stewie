import base64
import json
import requests
import sys

from server import *   #  GET KEYS

# Workaround to support both python 2 & 3
try:
    import urllib.request, urllib.error
    import urllib.parse as urllibparse
except ImportError:
    import urllib as urllibparse

# ----------------- 0. SPOTIFY BASE URL ----------------

SPOTIFY_API_BASE_URL = 'https://api.spotify.com'
API_VERSION = "v1"
SPOTIFY_API_URL = "{}/{}".format(SPOTIFY_API_BASE_URL, API_VERSION)

# ----------------- 1. USER AUTHORIZATION ----------------

# spotify endpoints
SPOTIFY_AUTH_BASE_URL = "https://accounts.spotify.com/{}"
SPOTIFY_AUTH_URL = SPOTIFY_AUTH_BASE_URL.format('authorize')
SPOTIFY_TOKEN_URL = SPOTIFY_AUTH_BASE_URL.format('api/token')
CLIENT_ID = 'bbba51ab47f34c39a9e9bc7503d73992'
CLIENT_KEY = '39e30e7a896342a097891f855d004765'
# server side parameter
# * fell free to change it if you want to, but make sure to change in
# your spotify dev account as well *
CLIENT_SIDE_URL = "http://0.0.0.0"
PORT = 5000
REDIRECT_URI = "{}:{}/callback/".format(CLIENT_SIDE_URL, PORT)
SCOPE = "playlist-modify-public playlist-modify-private user-read-recently-played user-top-read"
STATE = ""
SHOW_DIALOG_bool = True
SHOW_DIALOG_str = str(SHOW_DIALOG_bool).lower()


# https://developer.spotify.com/web-api/authorization-guide/
auth_query_parameters = {
    "response_type": "code",
    "redirect_uri": REDIRECT_URI,
    "scope": SCOPE,
    # "state": STATE,
    # "show_dialog": SHOW_DIALOG_str,
    "client_id": CLIENT_ID
}

#python 3
if sys.version_info[0] >= 3:
    URL_ARGS = "&".join(["{}={}".format(key, urllibparse.quote(val))
                    for key, val in list(auth_query_parameters.items())])


AUTH_URL = "{}/?{}".format(SPOTIFY_AUTH_URL, URL_ARGS)

'''
    This function must be used with the callback method present in the
    ../app.py file.
    And of course this will only works if ouath == True
'''


def authorize(auth_token):

    code_payload = {
        "grant_type": "authorization_code",
        "code": str(auth_token),
        "redirect_uri": REDIRECT_URI
    }
    print('hi')
    #python 3 or above
    if sys.version_info[0] >= 3:
        base64encoded = base64.b64encode(("{}:{}".format(CLIENT_ID, CLIENT_KEY)).encode())
        headers = {"Authorization": "Basic {}".format(base64encoded.decode())}
    else: 
        base64encoded = base64.b64encode("{}:{}".format(CLIENT_ID, CLIENT_KEY))
        headers = {"Authorization": "Basic {}".format(base64encoded)}

    post_request = requests.post(SPOTIFY_TOKEN_URL, data=code_payload,
                                 headers=headers)
    print('h3')
    # tokens are returned to the app
    response_data = json.loads(post_request.text)
    access_token = response_data["access_token"]

    # use the access token to access Spotify API
    auth_header = {"Authorization": "Bearer {}".format(access_token)}
    return auth_header



## FOR GET THE USER

## FOR FACE RECOGNITION
def get_tracks_from_playlist_call(id, token):
    url = 'https://api.spotify.com/v1/playlists/'+ id + '/tracks'
    headers  = { 'Authorization': 'Bearer ' + token, 'Accept': 'application/json', 'Content-Type': 'application/json' }
    response = requests.get(url, headers=headers )
    return response.text

def get_track_info_call(id,token):
    url = 'https://api.spotify.com/v1/audio-features?ids=' + id
    headers  = { 'Authorization': 'Bearer ' + token, 'cache-control': "no-cache", 'Content-type': 'application/json', 'Accept': 'application/json' }
    response = requests.get(url,data='', headers=headers)
    return response.text


## FOR USER EXPERIENCE
def get_list_playlists_call(token):
    url = 'https://api.spotify.com/v1/me/playlists'
    headers  = { 'Authorization': 'Bearer ' + token }
    response = requests.post(url, headers=headers)

    return response.text

def get_available_devices(token):
    url = "https://api.spotify.com/v1/me/player/devices"

    querystring = {"": ""}

    payload = ""
    headers = {
        'Authorization': "Bearer BQBIFLVNNTMuu9AYDmNKe0OOQHpqB2HYP2aILPBVRwyr9ZQmYcX_rmv3XkFM3vl-S1aa0zKLybEL9XHSp2QwGLoX3s2BWJ8Igh9b9tLCd0qyzVcv4mMw86wRpYF393s-MmIEc60P-7audDvocZMaEJRC_R8",
        'cache-control': "no-cache",
        'Postman-Token': "a49d621d-587a-4645-9a8d-2fa4c7e5e954"
    }

    response = requests.get(url, data = "", headers=headers, params=querystring)
    print(response.text)