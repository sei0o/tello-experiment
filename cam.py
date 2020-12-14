import time

import cv2
import easytello

tello = easytello.tello.Tello()
tello.takeoff()

time.sleep(2)

tello.send_command('streamon')
time.sleep(2)

cap = cv2.VideoCapture('udp://0.0.0.0:11111')

frame_width: int = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
frame_height: int = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

print(f'frame size: (width: {frame_width}, height: {frame_height})')

while True:
    ret, frame = cap.read()

    if not ret:
        print('empty frame')
        continue

    cv2.imshow('frame', frame)

    # land on Q key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        tello.land()
        break

cap.release()
cv2.destroyAllWindows()
