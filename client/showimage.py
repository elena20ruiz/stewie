import cv2
import os

if __name__ == '__main__':
    while 1:
        if os.path.exists("../server/token.txt"):
            img = cv2.imread("../server/imgtmp.jpg")
            cv2.imshow("Emotion recognizer", img)
            cv2.waitKey(1)
            os.remove("../server/token.txt")