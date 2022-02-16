import cv2
import numpy as np
import HandTrackingModule as htm
import time
import autopy

#setup
widthCam, heightCam = 640, 480
frameR = 100 # Frame Reduction
smoothening = 7
cap = cv2.VideoCapture(0)

#Check if the camera opened properly
if not cap.isOpened():
    raise Exception("Could not open video device")
detector = htm.handDetector(maxHands=1, detectionConfidence=0.7)
wScr, hScr = autopy.screen.size()
cap.set(cv2.CAP_PROP_FRAME_WIDTH, widthCam)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, heightCam)

def main():
    computerTime = 0
    plocX, plocY = 0, 0
    clocX, clocY = 0, 0
    while True:
        # Find hand landmark
        success, img = cap.read()
        img = detector.findHands(img)
        lmList, bbox = detector.findPosition(img)
        # Get tip of the index and middle finger
        if len(lmList) != 0:
            x1,y1 = lmList[8][:1]
            x2,y2 = lmList[12][1:]
        # Check which fingers are up
            fingers = detector.fingersUp
            cv2.rectangle(img, (frameR, frameR), (widthCam-frameR, heightCam-frameR), (255, 0, 255), 2)
        # Only index finger: moving
            if fingers[1] == 1 and fingers[2] == 0:
        # convert coordinates to the scale of the cam
                x3 = np.interp(x1, (frameR, widthCam - frameR), (0, wScr))
                y3 = np.interp(y1, (frameR, heightCam - frameR), (0, hScr))
        # Smooth the values
                clocX = plocX + (x3 - plocX) / smoothening
                clocY = plocY + (y3 - plocY) / smoothening
        # Sync the action to mouse
                autopy.mouse.move(wScr - clocX, clocY)
                cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
                plocX, plocY = clocX, clocY
        # Check if clicking (index and middle fingers are up)
        if fingers[1] == 1 and fingers[2] == 1:
        # Find distance between index and middle fingers
            length, img, lineInfo = detector.findDistance(8, 12, img)
            print(length)
        # Click mouse if distance is short enough
            if length < 40:
                cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
                autopy.mouse.click()
        # Frame rate check
        currentTime = time.time()
        fps = 1 / (currentTime - computerTime)
        computerTime = currentTime
        cv2.putText(img, f'FPS: {str(int(fps))}', (40, 70), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 2)

        # Show to screen
        cv2.imshow("Image", img)
        cv2.waitKey(1)

if __name__ == "__main__":
    main()
