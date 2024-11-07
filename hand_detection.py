import cv2 as cv
import mediapipe as mp


# Hand object
mpHands = mp.solutions.hands
hands = mpHands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5)

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

    # Acces the hands and draw their lanmarks
    if results.multi_hand_landmarks:
        for hand in results.multi_hand_landmarks:
            mpDraw.draw_landmarks(frame, hand, mpHands.HAND_CONNECTIONS)

    # image shape
    frame_height, frame_width, _ = frame.shape

    # Get the pos of the indexes
    if results.multi_hand_landmarks:
        for hand in results.multi_hand_landmarks:
            for Id, lm in enumerate(hand.landmark):
                pixelLm = mpDraw._normalized_to_pixel_coordinates(lm.x, lm.y, frame_width, frame_height)

                # index finger
                if Id == 8:
                    cv.circle(img=frame, center=(pixelLm[0], pixelLm[1]), radius=25, color=(234, 98, 91), thickness=-1)
                    

    # display
    cv.imshow("Web camera", frame)
    if cv.waitKey(1) & 0xFF == ord("q"):
        break
    
    
# clean
wc.release()
cv.destroyAllWindows()
