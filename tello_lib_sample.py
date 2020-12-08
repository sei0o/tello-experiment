from tello_lib import Tello, Coordinate, Direction
import time

t = Tello()
t.command()
time.sleep(3)
# t._send_command("wifi?")
t._send_command("wifi aaa bbb")
time.sleep(3)
# t._send_command("sdk?")
t.takeoff()
time.sleep(6)
# time.sleep(6)
# t.move(Direction.FORWARD, 80)
# time.sleep(1)
# print(t.speed)
time.sleep(3)
# t.land()
