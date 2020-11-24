from easytello import tello
import cv2
import numpy as np
import time

# TELLO = False
TELLO = True

if TELLO:
    d = tello.Tello()
    d.takeoff()
    time.sleep(2)

    d.up(400)
    time.sleep(2)

    # Do NOT use streamon() because it automatically takes control of the video stream (look at the source code)
    # d.streamon()
    d.send_command('streamon')  
    time.sleep(2)

stop_thres = 0.30

cap = None
if TELLO:
    cap = cv2.VideoCapture('udp://0.0.0.0:11111')
    # cap.set(cv2.CAP_PROP_FPS, 10)
else:
    cap = cv2.VideoCapture(0)

fw = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
fh = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

print(fw, fh)

while True:
  ret, frame = cap.read()

  if not ret:
    print('empty frame')
    continue


  cv2.imshow('frame', frame)

  # land on Q key
  if cv2.waitKey(1) & 0xFF == ord('q'):
      d.land()
      break

cap.release()
cv2.destroyAllWindows()