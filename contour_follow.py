from easytello import tello
import face_recognition
import cv2
import numpy as np
import time
import util

# TELLO = False
TELLO = True

if TELLO:
    d = tello.Tello()
    d.takeoff()
    print(d.send_command("battery?"))
    # time.sleep(2)

    # d.up(200)
    # time.sleep(2)

    # Do NOT use streamon() because it automatically takes control of the video stream (look at the source code)
    d.streamon()
    # d.send_command('streamon')  
    time.sleep(2)
    # d.land()

stop_thres = 0.30

# cap = None
# if TELLO:
#     cap = cv2.VideoCapture('udp://0.0.0.0:11111')
#     # cap.set(cv2.CAP_PROP_FPS, 10)
# else:
#     cap = cv2.VideoCapture(0)

# fw = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
# fh = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

# if not cap.isOpened():
#   print("Failed to open VideoCapture, stopping.")
#   exit(-1)

cv2.namedWindow("square")


process_this_frame = True
green = 0
# operating = False

while True:
    # Grab a single frame of video
    # ret, frame = cap.read()
    frame = d.frame


    # if TELLO:
    #   frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    if frame is None:
        continue

    fw = d.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    fh = d.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

    # Only process every other frame of video to save time
    # frame = np.fliplr(frame)
    hsv = cv2.cvtColor(frame ,cv2.COLOR_BGR2HSV)

    # green
    lowerb = np.array([40,30,90])
    upperb = np.array([90,255,255])
    mask = cv2.inRange(hsv, lowerb, upperb)

    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((3,3),np.uint8)) # remove noise
    green = cv2.countNonZero(mask)

    mask = cv2.bitwise_not(mask) # invert

    res = cv2.bitwise_and(frame,frame,mask=mask)

    # see: https://stackoverflow.com/questions/44522012/rectangle-detection-tracking-using-opencv
    contours = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[-2]
    bboxes = []
    dst = frame.copy()
    # dst = mask.copy()
    bboxmax = None
    areamax = 0
    for cnt in contours:
        bbox = cv2.boundingRect(cnt)
        x,y,w,h = bbox
        # w == fw means the entire frame
        if w<30 or h<30 or w==fw:
            continue
        area = w * h
        
        if areamax < area:
            bboxmax = bbox
            areamax = area

        cv2.rectangle(dst, (x,y), (x+w,y+h), (255,255,0), 3, 16)

    if not bboxmax:
        print("No Contours Found")
        continue

    x,y,w,h = bboxmax
    cx = int(x + w / 2)
    cy = int(y + h / 2)
    cv2.circle(dst, (cx,cy), 10, (0,0,255), 3)

    print(bboxmax)

    ratio = green / (fw * fh)
    print(ratio)

    if TELLO:
        if ratio > stop_thres:
            print("Exceeded")
            d.flip("b")
            d.stop()

        # d.curve(0, 0, 0, )
        # ターゲット中心がカメラ中心より右にあったら
        forward = True
        if cx - fw / 2 > 50:
            forward = False
            print("Going Right...")
            d.right(30)
            time.sleep(2)
        elif cx - fw / 2 < -50:
            forward = False
            print("Going Left...")
            d.left(30)
            time.sleep(2)

        if cy - fh / 2 > 50:
            forward = False
            print("Going Down...")
            d.down(30)
            time.sleep(2)
        elif cy - fh / 2 < -50:
            forward = False
            print("Going Up...")
            d.up(30)
            time.sleep(2)

        if forward:
            print("Going forward...")
            d.forward(50)

    # r = cv2.addWeighted(dst, 0.5, mask, 0.5, 0.0, None, None) 
    # cv2.imshow('res',r)
    # cv2.imshow('dst', dst)

    # land on Q key
    key = cv2.waitKey(0) & 0xFF
    if key == ord('q'):
        d.land()
        break

    if key == ord('r'):
        cv2.imshow('dst', frame)
        break

    util.key_to_move(d, key)

# Release handle to the webcam
d.cap.release()
cv2.destroyAllWindows()
