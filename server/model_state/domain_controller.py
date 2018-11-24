import server.stewie.model_training.model_training as mt
import server.stewie.spotify_api.controller as sc
import server.stewie.face_analysis as fa
import server.stewie.ms_api as ms

class DomainController:
    Client_ID = 'fc76e2af23f6481b8fee3a103be06bdc'
    Client_Secret = '58a174d9829a4bfcaa3e159c7131e88d'

    token = "BQBIFLVNNTMuu9AYDmNKe0OOQHpqB2HYP2aILPBVRwyr9ZQmYcX_rmv3XkFM3vl-S1aa0zKLybEL9XHSp2QwGLoX3s2BWJ8Igh9b9tLCd0qyzVcv4mMw86wRpYF393s-MmIEc60P-7audDvocZMaEJRC_R8"

    model = None
    TRAINING_SET_FILE = "TargetTrainingDataSet.txt"
    TRAINING_TARGET_JSON = "TrainingTarget.json"
    TRAINING_FEATURES_JSON = "TrainingFeatures.json"
    TRAINING_PATH = "model_training/"
    USER_PLAYLIST_ID = '574wL0I3ntRPvVVyNHriFK'
    TRAINING_PLAYLIST_ID = '1byvBifDJy7tqBrMJQgFZ1'
    playlistID = None
    playlistEmotion =


    def __init__(self, token):
        self.token = token
        self.getEmotionPredictionModel()

    def getTrackEmotionPrediction(self, id, model):
        trackJSON = sc.get_info_track(id, self.token)
        return mt.predictTrackEmotion(model, trackJSON)

    def getEmotionPredictionModel(self):
        data = sc.get_playlists_tracks(self.TRAINING_PLAYLIST_ID, self.token)
        sc.get_info_tracks(self.TRAINING_PATH + self.TRAINING_FEATURES_JSON, self.token, data)
        json_features_data = mt.getTrackJSONFromPath(self.TRAINING_PATH, self.TRAINING_FEATURES_JSON)

        json_target_data = mt.convertTargetInformationToJSON(self.TRAINING_PATH + self.TRAINING_SET_FILE)
        mt.saveJSONToPath(self.TRAINING_PATH, self.TRAINING_TARGET_JSON, json_target_data)

        training_json = mt.mergeTrackJSONFields(json_features_data, json_target_data)
        self.model = mt.generateTracksRegresionModel(training_json, mt.trackFeatures, mt.emotions)

    def computePlaylistEmotionPrediction(self):
        id = sc.get_user_playlistID(self.token)
        if id is None:
            print("User doesn't have an active playlist!")
        data = sc.get_playlists_tracks(self.TRAINING_PLAYLIST_ID, self.token)
        sc.get_info_tracks(self.TRAINING_PATH + self.TRAINING_FEATURES_JSON, self.token, data)
        json_features_data = mt.getTrackJSONFromPath(self.TRAINING_PATH, self.TRAINING_FEATURES_JSON)






# user-read-recently-played user-top-read user-follow-read user-follow-modify user-modify-playback-state user-read-playback-state user-read-currently-playing user-library-read user-library-modify user-read-private user-read-birthdate user-read-email playlist-modify-public playlist-read-collaborative playlist-modify-private playlist-read-private streaming app-remote-control
if __name__ == '__main__':
    DC = DomainController()
    model = DC.getEmotionPredictionModel()
    id = '3cfOd4CMv2snFaKAnMdnvK'
    print(DC.getTrackEmotionPrediction(id, model))