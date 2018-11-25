import json
from pprint import pprint

from server.spotify import calls


# TODO: Generate API Call in order to get all user playlists
def get_playlists(token):
    pass

# Return for each track id + name


def get_playlists_tracks(id_playlist, token):
    data = calls.get_tracks_from_playlist_call(id_playlist, token)
    d = data
    result = {'list': []}
    for item in d['items']:
        track = {
            'id': item['track']['id'],
            'name': item['track']['name']
        }
        result['list'].append(track)
    # with open('server/stewie/calls_api/songs.json', 'w') as outfile:
    #   json.dump(result, outfile)
    return result

# Get info track from list of traks


def get_info_tracks(data, token):
    print(data)
    input_ids = ''
    for track in data["list"]:
        input_ids += track['id'] + ','
    input_ids = input_ids[:-1]
    result = calls.get_track_info_call(input_ids, token)
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

# Get info track from list of traks


def get_info_track(track_id, token):
    result = calls.get_track_info_call(track_id, token)
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

# Get id of tablet device


def get_id_of_tablet(response):
    for device in response['devices']:
        if device['type'] == 'Smartphone':
            return device['id']
    else:
        return '-1'


def get_current_playlist_from_info(response):
    uri = response['context']['href']
    print('URI:   ' + uri)
    split_uri = uri.split('/')
    return split_uri[5]

