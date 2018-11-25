import cv2
import os

if __name__ == '__main__':
    while 1:
        if os.path.exists("token.txt"):
            img = cv2.imread("imgtmp.jpg")
            cv2.imshow("Emotion recognizer", img)
            os.remove("token.txt")