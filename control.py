# CLI-based controllers for Tello

from easytello import tello
import cv2
import numpy as np
import time
import util
from joystick import Controller

# TELLO = False
TELLO = True
STEP = 50

if TELLO:
  d = tello.Tello()
  d.takeoff()
  time.sleep(2)

  # d.up(400)
  # time.sleep(2)

  # Do NOT use streamon() because it automatically takes control of the video stream (look at the source code)
  # d.send_command('streamon')  
  time.sleep(2)

stop_thres = 0.30

# cap = None
# if TELLO:
#   cap = cv2.VideoCapture('udp://0.0.0.0:11111')
#   # cap.set(cv2.CAP_PROP_FPS, 10)
# else:
#   cap = cv2.VideoCapture(0)

cv2.namedWindow("square")

# fw = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
# fh = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

# print(fw, fh)

controller = Controller()

while True:
  # ret, frame = cap.read()

  # if not ret:
  #   print('empty frame')
  #   continue

  # cv2.imshow('frame', frame)

  # key = cv2.waitKey(0) & 0xff

  # if key == ord('q'):
  #   d.land()
  #   break

  # util.key_to_move(d, key)

  controller.get_state()
  if controller.changed:
    controller.stabilize()
    print(controller.command)
    d.send_command(controller.command)
    controller.changed = False
  

cap.release()
cv2.destroyAllWindows()