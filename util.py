STEP = 50


def key_to_move(d, key):
    if key == ord('t'):
        d.takeoff()

    if key == ord('l'):
        d.land()

    if key == ord('x'):
        d.stop()

    if key == ord('w'):
        d.forward(STEP)

    if key == ord('a'):
        d.left(STEP)

    if key == ord('s'):
        d.back(STEP)

    if key == ord('d'):
        d.right(STEP)

    if key == ord('e'):
        d.ccw(45)

    if key == ord('r'):
        d.cw(45)

    if key == ord('v'):
        d.flip("b")

    if key == ord('f'):
        d.rc_control(0, 20, 0, 0)

    if key == ord('v'):
        d.rc_control(0, -20, 0, 0)

    if key == ord('n'):
        d.rc_control(0, 0, 0, 0)

    if key == ord('u'):
        d.rc_control(0, 0, 10, 0)

    if key == ord('y'):
        d.rc_control(0, 0, 0, 30)