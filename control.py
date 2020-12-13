# CLI-based controllers for Tello

import cv2
import easytello

from joystick import Controller

STEP = 50

tello = easytello.tello.Tello()

cv2.namedWindow("square")

controller = Controller()

while True:
    controller.get_state()

    if controller.changed:
        controller.stabilize()
        print('sending command:', controller.command)
        tello.send_command(controller.command)
        controller.changed = False

cap.release()
cv2.destroyAllWindows()
