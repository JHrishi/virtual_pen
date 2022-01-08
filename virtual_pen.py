import cv2 as cv
import mediapipe as mp
import time
cap = cv.VideoCapture(0)
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

pTime = 0
cTime = 0


def draw(mypoints):
    for point in mypoints:
        cv.circle(result, (point[0], point[1]), 5, (0, 255, 0), cv.FILLED)


newpoints = []

while True:
    success, img = cap.read()
    img = cv.flip(img, 1)
    result = img.copy()
    imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
                if id == 8:
                    cv.circle(result, (cx, cy), 10, (0,0,255),cv.FILLED)
                    count = 0
                    if cx != 0 and cy != 0:
                        newpoints.append([cx, cy])
                    count += 1

    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime
    cv.putText(img, str(int(fps)), (10, 70), cv.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
    if len(newpoints) != 0:
        draw(newpoints)
    pTime = cTime
    cv.imshow('Image', result)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv.destroyAllWindows()
