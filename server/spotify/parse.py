import json
from pprint import pprint

from stewie.server.spotify_api import api as spotify


#TODO: Generate API Call in order to get all user playlists
def get_playlists(token):
    pass

# Return for each track id + name
def get_playlists_tracks(id_playlist,token):
    data = spotify.get_tracks_from_playlist_call(id_playlist, token)
    d = json.loads(data)
    result = { 'list' : [] }
    for item in d['items']:
        track = {
            'id': item['track']['id'],
            'name': item['track']['name']
        }
        result['list'].append(track)
    #with open('server/stewie/spotify_api/songs.json', 'w') as outfile:  
    #   json.dump(result, outfile)
    return result  

# Get info track from list of traks 
def get_info_tracks(path_tracks, token, data):
    #with open(path_tracks) as f:
    #    data = json.load(f)
    #pprint(data)

    input_ids = ''
    for track in data["list"]:
        input_ids += track['id'] + ','
    input_ids = input_ids[:-1]
    result = spotify.get_track_info_call(input_ids, token)
    result_file = {}
    d = json.loads(result)
    for item in d['audio_features']:
        res = {
            'danceability': item['danceability'],
            'energy': item['energy'],
            'mode': item['mode'],
            'time_signature': item['time_signature'],
            'acousticness': item['acousticness'],
            'instrumentalness': item['instrumentalness'],
            'liveness': item['liveness'],
            'loudness': item['loudness'],
            'speechiness': item['speechiness'],
            'valence': item['valence'],
            'tempo': item['tempo']
        }
        result_file[item['id']] = res
    with open(path_tracks, 'w') as outfile:
        json.dump(result_file, outfile)
    return result_file

# Get info track from list of traks
def get_info_track(track_id, token):
    result = spotify.get_track_info_call(track_id, token)
    result_file = {}
    d = json.loads(result)
    for item in d['audio_features']:
        res = {
            'danceability': item['danceability'],
            'energy': item['energy'],
            'mode': item['mode'],
            'time_signature': item['time_signature'],
            'acousticness': item['acousticness'],
            'instrumentalness': item['instrumentalness'],
            'liveness': item['liveness'],
            'loudness': item['loudness'],
            'speechiness': item['speechiness'],
            'valence': item['valence'],
            'tempo': item['tempo']
        }
        result_file[item['id']] = res
    return result_file

if __name__ == '__main__':
    token = 'BQB2aTNXJDcX1h57iy7Camn8SSIFOP7DN9I3x0s47aEWs2QCq_HtQ9EfS1kTLxlyn0xBdDpeWk1tnEbFOLj1DVfMLHpMUpYs5lyFLmHdtcPvJPT9-vWhjfvg4PUBmEFNgt5fsKs_H1iInAn4X_LOS2A'
    path_tracks = 'server/stewie/spotify_api/songs_copy.json'
    id_s = '1byvBifDJy7tqBrMJQgFZ1'
    data = get_playlists_tracks(id_s,token)
    get_info_tracks(path_tracks,token,data)