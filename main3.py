import cv2 as cv
import numpy as np
import mediapipe as mp
import time
import random
import colors as c
import math

# Hand object
mpHands = mp.solutions.hands
hands = mpHands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5)

# Landmarks display
mpDraw = mp.solutions.drawing_utils

# webcam
wc = cv.VideoCapture(0)

# score
score = 0

# random enemy coordinates
red_x = random.randint(a=50,b=600)
red_y = random.randint(a=50,b=600)

green_x = random.randint(a=50,b=600)
green_y = random.randint(a=50,b=600)

# Timer variables
timer_duration = 20  # 20 seconds timer
start_time = time.time()  # Record the start time

# Function to calculate distance between two points
def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

while wc.isOpened():
    # read
    _, frame = wc.read()

    # flip the frame
    frame = cv.flip(src=frame, flipCode=1)

    # convert RGB
    rgb_frame = cv.cvtColor(src=frame, code=cv.COLOR_BGR2RGB)

    # process the image
    results = hands.process(rgb_frame)

    # Access the hands and draw their landmarks
    if results.multi_hand_landmarks:
        for hand in results.multi_hand_landmarks:
            mpDraw.draw_landmarks(frame, hand, mpHands.HAND_CONNECTIONS, mpDraw.DrawingSpec(color=c.red, circle_radius=4))

    # image shape
    frame_height, frame_width, _ = frame.shape
    
    # draw red and green circles
    red_radius = 40
    green_radius = 45
    cv.circle(img=frame, center=(red_x, red_y), radius=red_radius, color=c.red, thickness=10)
    cv.circle(img=frame, center=(green_x, green_y), radius=green_radius, color=c.green, thickness=10)
    cv.putText(img=frame, text="score: "+str(score), org=(100, 120), fontFace=cv.FONT_HERSHEY_SIMPLEX, fontScale=3, color=c.blue, thickness=3)

    # Calculate the remaining time
    elapsed_time = time.time() - start_time
    remaining_time = max(0, int(timer_duration - elapsed_time))  # Ensure the remaining time doesn't go negative
    cv.putText(img=frame, text=f"Time Left: {remaining_time}s", org=(500, 120), fontFace=cv.FONT_HERSHEY_SIMPLEX, fontScale=2, color=c.blue, thickness=2)

    # If time is up, end the game
    if remaining_time == 0:
        cv.putText(img=frame, text="Time's up!", org=(300, 300), fontFace=cv.FONT_HERSHEY_SIMPLEX, fontScale=5, color=c.red, thickness=5)
        cv.imshow("Web camera", frame)
        cv.waitKey(2000)  # Show "Time's up!" for 2 seconds
        break

    # Get the positions of the hand landmarks
    if results.multi_hand_landmarks:
        for hand in results.multi_hand_landmarks:
            for Id, lm in enumerate(hand.landmark):
                pixelLm = int(lm.x * frame_width), int(lm.y * frame_height)

                # index finger (Id 8 is the tip of the index finger)
                if Id == 8:
                    cv.circle(img=frame, center=(pixelLm[0], pixelLm[1]), radius=40, color=c.olive, thickness=-10)

                    # Calculate the distance from the index finger to the center of the circles
                    red_distance = distance(pixelLm, (red_x, red_y))
                    green_distance = distance(pixelLm, (green_x, green_y))

                    # Check if the finger is close to the red or green circle
                    if red_distance <= red_radius:  # Finger is inside red circle
                        print("Oh no!")
                        red_x = random.randint(a=50,b=600)
                        red_y = random.randint(a=50,b=600)
                        score -= 1
                        
                    if green_distance <= green_radius:  # Finger is inside green circle
                        print("Gotcha!")
                        red_x = random.randint(a=50,b=600)
                        red_y = random.randint(a=50,b=600)
                        green_x = random.randint(a=50, b=600)
                        green_y = random.randint(a=50, b=600)
                        score += 1

    # display the frame
    cv.imshow("Web camera", frame)
    
    if cv.waitKey(1) & 0xFF == ord("q"):
        break

# clean up
wc.release()
cv.destroyAllWindows()
