import cv2
import mediapipe as mp
import time

#start the camera
cap = cv2.VideoCapture(0)   

#creates a hand object
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

#time to calculate fps 
computerTime = 0
currentTime = 0

while True:
    success, img = cap.read()
    #convert to rbg
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    #process the hand information
    results = hands.process(imgRGB)
    #print(results.multi_hand_landmarks)
    if results.multi_hand_landmarks:
        for handLMs in results.multi_hand_landmarks:
            for id, lm in enumerate(handLMs.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
                print(id, cx, cy)
                if id == 8:
                    cv2.circle(img, (cx, cy), 25, (255, 0, 255), cv2.FILLED)

            mpDraw.draw_landmarks(img, handLMs, mpHands.HAND_CONNECTIONS)
    
    currentTime = time.time()
    fps = 1 / (currentTime - computerTime)
    computerTime = currentTime 
    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_COMPLEX, 3, (255, 0, 255), 3)

    cv2.imshow("Image", img)
    cv2.waitKey(1)
