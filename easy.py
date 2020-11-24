from easytello import tello
import time
import cv2


d = tello.Tello()
d.takeoff()
time.sleep(3)

d.streamon()

# for i in range(4):
# 	d.forward(100)
# 	d.cw(90)

time.sleep(10)

d.land()
# Turning on stream
# Turning off stream
# d.streamoff()

cap = cv2.VideoCapture('udp://0.0.0.0:11111')
if not cap.isOpened():
  print("Failed to open VideoCapture, stopping.")
  exit(-1)

while True:
  ret, frame = cap.read()

  if not ret:
    print('empty frame')
    break 

  cv2.imshow('image', frame)
  if cv2.waitKey(1) & 0xFF == ord('q'):
    break

cap.release()
cv2.destroyAllWindows()
