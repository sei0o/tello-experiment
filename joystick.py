import threading

import pygame
from pygame.locals import *


class Controller:
    def __init__(self):

        # initialize joystick
        pygame.joystick.init()
        try:
            # create joystick instance
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()
            print('The name of Joystick:', self.joystick.get_name())
            print('The number of buttons:', self.joystick.get_numbuttons())
        except pygame.error:
            print('No joystick found')
            exit(1)

        pygame.init()
        self.screen = pygame.display.set_mode((320, 320))

        self.a = False
        self.b = False
        self.x = False
        self.y = False

        self.changed = False

        self.left_x = self.left_y = self.right_x = self.right_y = 0.0

    def get_state(self):
        for e in pygame.event.get():
            if e.type == pygame.locals.JOYAXISMOTION:
                self.left_x, self.left_y, _, self.right_x, self.right_y = (self.joystick.get_axis(i) for i in range(5))
                self.changed = True
            if e.type == pygame.locals.JOYBUTTONDOWN:
                self.changed = not self.__getattribute__("abxy"[e.button])
                self.__setattr__("abxy"[e.button], True)
            if e.type == pygame.locals.JOYBUTTONUP:
                # self.changed = self.__getattribute__("abxy"[e.button])
                self.__setattr__("abxy"[e.button], False)

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
