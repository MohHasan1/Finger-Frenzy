import cv2 as cv
import numpy as np
import mediapipe as mp
from mediapipe.framework.formats import landmark_pb2
import time
import random
import colors as c

# Hand object
mpHands = mp.solutions.hands
hands = mpHands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5)

# Landmarks display
mpDraw = mp.solutions.drawing_utils

# webcam
wc = cv.VideoCapture(0)

# score
score = 0
# random enemy co-ordinate
red_x = random.randint(a=50,b=600)
red_y = random.randint(a=50,b=600)

green_x = random.randint(a=50,b=600)
green_y = random.randint(a=50,b=600)



def enemy(img):
    global score, red_x, red_y
    
    # draw the enemies
    cv.circle(img=img, center=(red_x, red_y), radius=40, color=c.green, thickness=10)




while wc.isOpened():
    # read
    _, frame = wc.read()

    # flip the frame
    frame = cv.flip(src=frame, flipCode=1)

    # convert RGB
    rgb_frame = cv.cvtColor(src=frame, code=cv.COLOR_BGR2RGB)

    # process the image
    results = hands.process(rgb_frame)

    # Acces the hands and draw their lanmarks
    if results.multi_hand_landmarks:
        for hand in results.multi_hand_landmarks:
            mpDraw.draw_landmarks(frame, hand, mpHands.HAND_CONNECTIONS, mpDraw.DrawingSpec(color=c.red, circle_radius=4))

    # image shape
    frame_height, frame_width, _ = frame.shape
    
    # enemy
    enemy(img=frame)
    cv.putText(img=frame, text="score: "+str(score), org=(100, 120), fontFace=cv.FONT_HERSHEY_SIMPLEX, fontScale=3, color=c.blue, thickness=3)

    # Get the pos of the indexes
    if results.multi_hand_landmarks:
        for hand in results.multi_hand_landmarks:
            for Id, lm in enumerate(hand.landmark):
                # pixelLm = mpDraw._normalized_to_pixel_coordinates(lm.x, lm.y, frame_width, frame_height)
                pixelLm = int(lm.x * frame_width), int(lm.y * frame_height)

                # index finger
                if Id == 8:
                    cv.circle(img=frame, center=(pixelLm[0], pixelLm[1]), radius=40, color=c.red, thickness=10)

                    if pixelLm[0] == red_x or pixelLm[0] == red_x + 10 or pixelLm[0] == red_x - 10 or pixelLm[1] == red_y or  pixelLm[1] == red_y-10 or  pixelLm[1] == red_y+10:
                        print("Gotcha")
                        red_x = random.randint(a=50,b=600)
                        red_y = random.randint(a=50,b=600)
                        score+=1
            

                        
                    
                    
    
    # display
    cv.imshow("Web camera", frame)
    if cv.waitKey(1) & 0xFF == ord("q"):
        break
    
    
# clean
wc.release()
cv.destroyAllWindows()
