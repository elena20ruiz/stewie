import server.model_training.model_training as mt
import server.spotify.parse as sc
import server.emotion.emotion_api as emotion
import numpy as np
from matplotlib import pyplot as plt
import cv2
import time
from collections import OrderedDict

class DomainController:
    Client_ID = 'fc76e2af23f6481b8fee3a103be06bdc'
    Client_Secret = '58a174d9829a4bfcaa3e159c7131e88d'

    emotions = ["anger", "contempt", "disgust", "fear", "happiness", "neutral", "sadness", "surprise"]
    token = "BQBIFLVNNTMuu9AYDmNKe0OOQHpqB2HYP2aILPBVRwyr9ZQmYcX_rmv3XkFM3vl-S1aa0zKLybEL9XHSp2QwGLoX3s2BWJ8Igh9b9tLCd0qyzVcv4mMw86wRpYF393s-MmIEc60P-7audDvocZMaEJRC_R8"
    model = None
    TRAINING_SET_FILE = "TargetTrainingDataSet.txt"
    TRAINING_TARGET_JSON = "TrainingTarget.json"
    TRAINING_FEATURES_JSON = "TrainingFeatures.json"
    TRAINING_PATH = "model_training/"
    USER_PLAYLIST_ID = '574wL0I3ntRPvVVyNHriFK'
    TRAINING_PLAYLIST_ID = '1byvBifDJy7tqBrMJQgFZ1'
    playlistID = None
    playlistTrackEmotions = None
    camera_window_name = "Emotion recognizer"
    emotionCamera = None
    cameraWidth = None
    cameraHeight = None
    TMP_IMG_PATH = "tmpimg.jpg"



    def __init__(self):
        #self.getEmotionPredictionModel()
        cv2.namedWindow(self.camera_window_name)
        self.emotionCamera = cv2.VideoCapture(0)
        img = self.get_webcam_image()
        height, width = img.shape[:2]
        self.cameraHeight = 300
        self.cameraWidth = self.cameraHeight * (width/height)


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
        for id, value in json_features_data:
            Y = mt.predictTrackEmotion(self.model, value)
            aux = [id]
            aux = aux + self.dict2list(Y)
            self.playlistTrackEmotions.append(aux)

    def processImage(self):
        img = self.get_webcam_image()
        img = cv2.resize(img, (int(DC.cameraWidth), int(DC.cameraHeight)))
        cv2.imwrite(self.TMP_IMG_PATH, img)
        response = emotion.get_image_emotion(self.TMP_IMG_PATH)
        if len(response) != 0:
            img = self.editImage(img, response[0]["faceRectangle"])
            emotionsQueryDict = response[0]["faceAttributes"]["emotion"]
            emotionsQueryList = self.dict2list(emotionsQueryDict)
            trackIDList = self.updatePlaylistOrder(emotionsQueryList)
        self.set_webcam_image(img)
        cv2.waitKey(1)

    def dict2list(self, dict):
        list = []
        for i in range(len(self.emotions)):
            list.append(dict[self.emotions[i]])
        return list

    def updatePlaylistOrder(self, emotionsQueryList):
        d = {}
        for i in range(len(self.playlistTrackEmotions)):
            sim = self.computeSimilarity(self.playlistTrackEmotions[i][1:], emotionsQueryList)
            d[self.playlistTrackEmotions[i][0]] = sim
        ordered_dict = OrderedDict(sorted(d.items(), key=lambda t: t[1]))



    def computeSimilarity(self, v1, v2):
        sum = 0
        for i in range (len(v1)):
            sum += v1[i] * v2[i]
        return sum

    def editImage(self, img, rectangleInfo):
        img = cv2.rectangle(img, (rectangleInfo["left"], rectangleInfo["top"]),
                            (rectangleInfo["left"] + rectangleInfo["width"],rectangleInfo["top"] + rectangleInfo["height"]),(0,255,0), 2)
        return img

    def get_webcam_image(self):
        s, img = self.emotionCamera.read()
        return img

    def set_webcam_image(self, img):
        cv2.imshow(self.camera_window_name, img)

    def destroy_camera(self):
        cv2.destroyWindow(self.camera_window_name)


# user-read-recently-played user-top-read user-follow-read user-follow-modify user-modify-playback-state user-read-playback-state user-read-currently-playing user-library-read user-library-modify user-read-private user-read-birthdate user-read-email playlist-modify-public playlist-read-collaborative playlist-modify-private playlist-read-private streaming app-remote-control
if __name__ == '__main__':
    DC = DomainController()
    #model = DC.getEmotionPredictionModel()
    while 1:
        DC.processImage()
        time.sleep(5)
     #print(DC.getTrackEmotionPrediction(id, model))