import time

import cv2
import easytello
import numpy as np

d = easytello.tello.Tello()
d.takeoff()
time.sleep(3)

# Do NOT use streamon() because it automatically takes control of the video stream (look at the source code)
d.send_command('streamon')
time.sleep(5)

stop_thres = 0.06

cap = cv2.VideoCapture('udp://0.0.0.0:11111')

frame_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
frame_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

process_this_frame = True
green = 0

while True:
    # Grab a single frame of video
    ret, frame = cap.read()

    if not ret:
        print('empty frame')
        continue

    # Only process every other frame of video to save time
    if process_this_frame:
        frame = np.fliplr(frame)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # green bounding
        color_bottom = np.array([50, 40, 30])
        color_top = np.array([80, 255, 255])
        mask = cv2.inRange(hsv, color_bottom, color_top)

        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))  # remove noise
        green = cv2.countNonZero(mask)

        mask = cv2.bitwise_not(mask)  # invert

        res = cv2.bitwise_and(frame, frame, mask=mask)

        # see: https://stackoverflow.com/questions/44522012/rectangle-detection-tracking-using-opencv
        contours = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[-2]

        dst = frame.copy()
        for cnt in contours:
            bbox = cv2.boundingRect(cnt)
            x, y, w, h = bbox
            # big enough and not too big
            if w < 30 or h < 30 or w * h < 2000 or w > 500:
                continue

            cv2.rectangle(dst, (x, y), (x + w, y + h), (255, 0, 0), 1, 16)

        cv2.imshow('mask', mask)
        cv2.imshow('dst', dst)

    process_this_frame = not process_this_frame

    # Stop if the ratio of green exceeds the threshold
    ratio = green / (frame_width * frame_height)
    if ratio > stop_thres:
        print(f'Exceeded. (ratio: {ratio})')
        d.land()

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
cap.release()
cv2.destroyAllWindows()
