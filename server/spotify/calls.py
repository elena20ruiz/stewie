import base64
import json
import requests
import sys
import pprint
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
CLIENT_SIDE_URL = "http://127.0.0."
PORT = 5000
REDIRECT_URI = "{}:{}/callback/".format(CLIENT_SIDE_URL, PORT)
SCOPE = "user-read-recently-played user-top-read user-follow-read user-follow-modify user-modify-playback-state user-read-playback-state user-read-currently-playing user-library-read user-library-modify user-read-private user-read-birthdate user-read-email playlist-modify-public playlist-read-collaborative playlist-modify-private playlist-read-private streaming app-remote-control"
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
    if "access_token" in response_data:
        access_token = response_data["access_token"]

        # use the access token to access Spotify API
        auth_header = {"Authorization": "Bearer {}".format(access_token)}
        return access_token
    else:
        return "There were a problem while obtaining Spotify token. Please, try again.s"



## FOR GET THE USER

## FOR FACE RECOGNITION
def get_tracks_from_playlist_call(id, token):
    print(str(id))
    url = 'https://api.spotify.com/v1/playlists/'+ str(id) + '/tracks'
    headers  = { 'Authorization': 'Bearer ' + token, 'Accept': 'application/json', 'Content-Type': 'application/json' }
    response = requests.get(url, headers=headers )
    return response.json()

def get_track_info_call(id,token):
    url = 'https://api.spotify.com/v1/audio-features?ids=' + str(id)
    headers  = { 'Authorization': 'Bearer ' + token, 'cache-control': "no-cache", 'Content-type': 'application/json', 'Accept': 'application/json' }
    response = requests.get(url,data='', headers=headers)
    return response.text


## FOR USER EXPERIENCE
def get_list_playlists_call(token):
    url = 'https://api.spotify.com/v1/me/playlists'
    headers  = { 'Authorization': 'Bearer ' + token }
    response = requests.post(url, headers=headers)
    return response.text

def get_available_devices(access_token):
    url = "https://api.spotify.com/v1/me/player/devices"
    headers  = { 'Authorization': 'Bearer ' + access_token }
    resp = requests.get(url, headers=headers)
    print(resp.text)
    return resp.json()

def change_dispositive(access_token):
    url = "https://api.spotify.com/v1/me/player/devices"
    headers  = { 'Authorization': 'Bearer ' + access_token }
    resp = requests.get(url, headers=headers)
    print(resp.text)
    return resp.json()

def get_current_playlist(access_token):
    url = 'https://api.spotify.com/v1/me/player'
    headers  = { 'Authorization': 'Bearer ' + access_token }
    resp = requests.get(url, headers=headers)
    print(resp.text)
    return resp.json()

def connect_to_device(access_token, device):
    url = 'https://api.spotify.com/v1/me/player'
    headers  = { 'Authorization': 'Bearer ' + access_token, 'Content-Type': 'application/json' }
    device_data = {
    "device_ids": [
        device
        ]
    }
    resp = requests.put(url, headers=headers, data=device_data)
    print(resp.text)
    return resp.json()

def reorder_playlist(playlist_id, list_tracks, token):
    current_position = get_tracks_from_playlist_call(playlist_id,token)
    #TODO: See how will get list_tracks
    item = list_tracks[0]
    pos = 0
    for original in current_position['items']:
        if item == original['id']:
            break
        else: 
            pos += 1
    body = {
    "range_start": pos,
    "range_length": 1,
    "insert_before": 1
    }
    url = 'https://api.spotify.com/v1/playlists/'+ playlist_id + '/tracks'
    headers  = { 'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json' }
    resp = requests.put(url, headers=headers, data=body)
    return resp.json()