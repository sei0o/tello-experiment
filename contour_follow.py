import easytello
import cv2
import numpy as np
import time
import util

tello = easytello.tello.Tello()
tello.takeoff()
tello.streamon()
time.sleep(2)

stop_threshold = 0.30

cv2.namedWindow('square')

process_this_frame = True
green = 0

while True:
    # easytello.tello.Tello will have an attribute `frame` after start Tello()._video_thread()
    frame = tello.frame

    if frame is None:
        continue

    frame_width = tello.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    frame_height = tello.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

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
    
    max_bounding_box = 0
    max_area = 0
    
    for cnt in contours:
        bbox = cv2.boundingRect(cnt)
        x, y, w, h = bbox
        # w == frame_width means the entire frame
        if w < 30 or h < 30 or w == frame_width:
            continue
        area = w * h

        if max_area < area:
            max_bounding_box = bbox
            max_area = area

        cv2.rectangle(dst, (x, y), (x + w, y + h), (255, 255, 0), 3, 16)

    if not max_bounding_box:
        print('No Contours Found')
        continue

    x, y, w, h = max_bounding_box
    cx = int(x + w / 2)
    cy = int(y + h / 2)
    
    cv2.circle(dst, (cx, cy), 10, (0, 0, 255), 3)

    ratio = green / (frame_width * frame_height)

    if ratio > stop_threshold:
        print(f'Exceeded threshold. (ratio: {ratio})')
        tello.flip('b')
        tello.stop()

    # if the center of target is on the right
    forward = True
    if cx - frame_width / 2 > 50:
        forward = False
        print('Going Right...')
        tello.right(30)
        time.sleep(2)
    # on the left
    elif cx - frame_width / 2 < -50:
        forward = False
        print('Going Left...')
        tello.left(30)
        time.sleep(2)

    # on the top
    if cy - frame_height / 2 > 50:
        forward = False
        print('Going Down...')
        tello.down(30)
        time.sleep(2)
    # on the bottom
    elif cy - frame_height / 2 < -50:
        forward = False
        print('Going Up...')
        tello.up(30)
        time.sleep(2)

    # if the target is in the center
    if forward:
        print('Going forward...')
        tello.forward(50)
        time.sleep(2)

    # land on Q key
    key = cv2.waitKey(0) & 0xFF
    if key == ord('q'):
        tello.land()
        break

    # show frame for debugging
    # r = cv2.addWeighted(dst, 0.5, mask, 0.5, 0.0, None, None) 
    # cv2.imshow('res',r)
    # cv2.imshow('dst', dst)
    
    if key == ord('r'):
        cv2.imshow('dst', frame)
        break

    util.key_to_move(tello, key)

# Release handle to the webcam
tello.cap.release()
cv2.destroyAllWindows()
