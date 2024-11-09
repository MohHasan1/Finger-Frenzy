"""""
This script uses OpenCV and MediaPipe to detect and track hand landmarks in real-time using a webcam. It captures 
video frames, processes them to detect hand landmarks, and displays the landmarks with the index finger highlighted.
Press 'q' to exit the webcam feed.

Recap:
1. Initialize MediaPipe's hand detection and landmark module.
2. Capture video frames from the webcam.
3. Convert each frame to RGB and process it with MediaPipe to detect hand landmarks.
4. Draw the hand landmarks on the frame.
5. Highlight the index finger by drawing a circle on the corresponding landmark.
6. Display the processed video in a window and allow exit with the 'q' key.
"""""

import cv2 as cv
import mediapipe as mp

# Hand module
mpHands = mp.solutions.hands
# Hand object
hands = mpHands.Hands()
# hands = mpHands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5)

# Landmarks display
mpDraw = mp.solutions.drawing_utils

# webcam
wc = cv.VideoCapture(0)

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
            mpDraw.draw_landmarks(frame, hand, mpHands.HAND_CONNECTIONS)

    # Get the image shape
    frame_height, frame_width, _ = frame.shape

    # Get the position of the index finger
    if results.multi_hand_landmarks:
        for hand in results.multi_hand_landmarks:
            # The x and y value are normalized (0-1)
            for Id, lm in enumerate(hand.landmark):
                pixelLm = mpDraw._normalized_to_pixel_coordinates(lm.x, lm.y, frame_width, frame_height)

                # Index finger
                if Id == 9:
                    cv.circle(img=frame, center=(pixelLm[0], pixelLm[1]), radius=25, color=(234, 98, 91), thickness=-1)

    # display
    cv.imshow("Web camera", frame)
    if cv.waitKey(1) & 0xFF == ord("q"):
        break

# clean
wc.release()
cv.destroyAllWindows()
