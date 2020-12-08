import threading

import pygame
from pygame.locals import *

# ジョイスティックの初期化
pygame.joystick.init()
try:
    # ジョイスティックインスタンスの生成
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    print('ジョイスティックの名前:', joystick.get_name())
    print('ボタン数 :', joystick.get_numbuttons())
except pygame.error:
    print('ジョイスティックが接続されていません')
    exit(1)

# pygameの初期化
pygame.init()

# 画面の生成
screen = pygame.display.set_mode((320, 320))

# ループ
active = True


class Controller:
    def __init__(self):
        self.a = False
        self.b = False
        self.x = False
        self.y = False

        self.changed = False

        self.left_x = self.left_y = self.right_x = self.right_y = 0.0

    def get_state(self):
        for e in pygame.event.get():
            if e.type == pygame.locals.JOYAXISMOTION:
                self.left_x, self.left_y, _, self.right_x, self.right_y = (joystick.get_axis(i) for i in range(5))
                self.changed = True
            if e.type == pygame.locals.JOYBUTTONDOWN:
                self.changed = not self.__getattribute__("abxy"[e.button])
                self.__setattr__("abxy"[e.button], True)
            if e.type == pygame.locals.JOYBUTTONUP:
                # self.changed = self.__getattribute__("abxy"[e.button])
                self.__setattr__("abxy"[e.button], False)
            if e.type == QUIT:
                active = False


    def stabilize(self):
        for attr in ("left_x", "left_y", "right_x", "right_y"):
            if abs(self.__getattribute__(attr)) < 0.01:
                self.__setattr__(attr, 0)

    @property
    def command(self):
        if self.a:
            return "takeoff"
        elif self.b:
            return "land"
        a = round(self.left_x * 100)
        b = round(self.left_y * -100)
        c = round(self.right_y * -100)
        d = round(self.right_x * 100)
        return "rc {} {} {} {}".format(a, b, c, d)


def show_state(controller: Controller):
    while active:
        # if controller.a:
        #     print("a")
        # if controller.b:
        #     print("b")
        # if controller.x:
        #     print("x")
        # if controller.y:
        #     print("y")
        if controller.changed:
            controller.stabilize()
            print(controller.command)
            # print(f"({controller.left_x}, {controller.left_y}), ({controller.right_x}, {controller.right_y})")
            controller.changed = False

# getter = threading.Thread(target=get_state, args=(controller,))
# shower = threading.Thread(target=show_state, args=(controller,))
# getter.start()
# shower.start()
# while active:
#    pass
# getter.join()
# shower.join()
