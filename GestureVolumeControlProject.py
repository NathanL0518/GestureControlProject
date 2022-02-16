import cv2
import time
import HandTrackingModule as htm
import numpy as np
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


#Initializing variables and the camera
cap = cv2.VideoCapture(0)

#Check if the camera opened properly
if not cap.isOpened():
    raise Exception("Could not open video device")
detector = htm.handDetector(detectionConfidence=0.7) 

#Libraries that can change the volume
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()
# volume.GetMasterVolumeLevel()
# volume.GetVolumeRange()
# volume.SetMasterVolumeLevel(-20.0, None)
volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]

#set resolution to 1080p
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)    

#Loop that does things
def main():
    computerTime = 0
    vol = 0
    volBar = 400
    volPer = 0
    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        lmList = detector.findPosition(img, draw=False)

        if len(lmList) != 0:
            x1, y1 = lmList[4][1], lmList[4][2]
            x2, y2 = lmList[8][1], lmList[8][2]
            cx, cy = (x1+x2)//2, (y1+y2)//2
            cv2.circle(img, (x1, y1), 25, (255, 255, 0), cv2.FILLED)
            cv2.circle(img, (x2, y2), 25, (255, 255, 0), cv2.FILLED)
            cv2.line(img, (x1, y1), (x2, y2), (200, 0, 200), 2)
            cv2.circle(img, (cx, cy), 25, (255, 255, 0), cv2.FILLED)
            length = math.hypot(x2 - x1, y2 - y1)

            #convert length to volume range
            vol = np.interp(length, [50, 300], [minVol, maxVol])
            volBar = np.interp(length, [50, 300], [400, 150]) 
            volPer = np.interp(length, [50, 300], [0, 100])

            #set volume
            volume.SetMasterVolumeLevel(vol, None)
            if length <= 50:
                cv2.circle(img, (cx, cy), 25, (0, 255, 0), cv2.FILLED)
            if length >= 300:
                cv2.circle(img, (cx, cy), 25, (255, 0, 0), cv2.FILLED)
        #volume bar
        cv2.rectangle(img, (50, 150), (85, 400), (0, 255, 0), 3)
        cv2.rectangle(img, (50, int(volBar)), (85, 400), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, f'Volume: {str(int(volPer))} %', (40, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)

        #Calculate fps and display it
        currentTime = time.time()
        fps = 1 / (currentTime - computerTime)
        computerTime = currentTime 
        cv2.putText(img, f'FPS: {str(int(fps))}', (40, 70), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)

        #display everything


if __name__ == "__main__":
    main()
