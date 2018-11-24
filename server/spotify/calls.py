import base64
import json
import requests
import sys


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