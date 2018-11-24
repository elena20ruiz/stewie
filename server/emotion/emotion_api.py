
import requests
import json
from server import *




headers  = {'Ocp-Apim-Subscription-Key': MICROSOFT_KEY, "Content-Type": "application/octet-stream" }

def get_image_emotion(image_path):
    image_data = open(image_path, "rb").read()
    url = MICROSOFT_URL + '?returnFaceId=true&returnFaceLandmarks=true&returnFaceAttributes=emotion'
    response = requests.post(url, headers=headers, data=image_data)
    response.raise_for_status()
    analysis = response.json()
    with open('server/emotion/emotion.json', 'w') as outfile:  
       json.dump(analysis, outfile)
    return analysis


if __name__ == '__main__':
    get_image_emotion('test.jpg')