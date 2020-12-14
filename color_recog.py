from easytello import tello
import face_recognition
import cv2
import numpy as np
import time
import util

TELLO = True # 実機であればTrue, PCによるデバッグ時にはFalseに設定

if TELLO:
    d = tello.Tello()
    d.takeoff()
    time.sleep(3)

    # Do NOT use streamon() because it automatically takes control of the video stream (look at the source code)
    # d.streamon()
    d.send_command('streamon')  
    time.sleep(5)
    # d.land()

stop_thres = 0.06

cap = None
if TELLO:
    cap = cv2.VideoCapture('udp://0.0.0.0:11111')
    # cap.set(cv2.CAP_PROP_FPS, 1)
else:
    cap = cv2.VideoCapture(0)

fw = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
fh = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

# if not cap.isOpened():
#   print("Failed to open VideoCapture, stopping.")
#   exit(-1)

process_this_frame = True
green = 0

while True:
    # Grab a single frame of video
    ret, frame = cap.read()

    if not ret:
        print('empty frame')
        continue

    # if TELLO:
    #   frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Only process every other frame of video to save time
    if process_this_frame:
      frame = np.fliplr(frame)
      hsv = cv2.cvtColor(frame ,cv2.COLOR_BGR2HSV)

      # green
      lowerb = np.array([50,40,30])
      upperb = np.array([80,255,255])
      mask = cv2.inRange(hsv, lowerb, upperb)

      mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((3,3),np.uint8)) # remove noise
      green = cv2.countNonZero(mask)

      mask = cv2.bitwise_not(mask) # invert 

      res = cv2.bitwise_and(frame,frame,mask=mask)

      # see: https://stackoverflow.com/questions/44522012/rectangle-detection-tracking-using-opencv
      contours = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[-2]
      bboxes = []
      dst = frame.copy()
      # print(contours)
      areasum = 0
      for cnt in contours:
          bbox = cv2.boundingRect(cnt)
          x,y,w,h = bbox
          if w<30 or h < 30 or w*h < 2000 or w > 500:
              continue
          area = w * h
          areasum += area

          cv2.rectangle(dst, (x,y), (x+w,y+h), (255,0,0), 1, 16)

      # print(areasum / (fw * fh))

      # Display the resulting image
      cv2.imshow('mask', mask)  
      cv2.imshow('dst', dst)  

    process_this_frame = not process_this_frame

    # Stop if the ratio of green exceeds the threshold
    ratio = green / (fw * fh)
    print(ratio)
    if ratio > stop_thres:
      print("Exceeded")
      d.land()

    # Hit 'q' on the keyboard to quit!
    key = cv2.waitKey(1)
    if key & 0xFF == ord('q'):
        break

    util.key_to_move(d, key)

# Release handle to the webcam
cap.release()
cv2.destroyAllWindows()
