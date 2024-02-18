import os
import math
import re
from enum import IntFlag

import pyautogui
import pygame

from imgui_window import State
from win32_input import PressKey, ReleaseKey

'''
Dualshock 4 axis mapping:

0 - left stick x (left -1, right 1)
1 - left stick y (up -1, down 1)
2 - right stick x (left -1, right 1)
3 - right stick y (up -1, down 1)
4 - L2 (-1 - 1)
5 - R2 (-1 - 1)

Buttons:

2 - square
0 - cross
1 - circle
3 - triangle
9 - L1
10 - R1
11 - dpad up
12 - dpad down
13 - dpad left
14 - dpad right
4 - share
6 - options
7 - L3
8 - R3
5 - PS button
15 - touchpad
'''

os.environ['SDL_JOYSTICK_ALLOW_BACKGROUND_EVENTS'] = '1'
# constants for the joystick events
AXIS_MOTION = 1536
BTN_DOWN = 1539
BTN_UP = 1540
KEY_MAP = {
    'S': 'b,c',
    'N': 'd,e',
    'W': 'f,g',
    'E': 'h,i',
    #'SW': ',',
    #'SE': ',',
    #'NE': ',',
    #'NW': ',',

    'A': 'j,k,l',
    'B': 'm,n,o',
    'C': 'p,q,r',
    'D': 's,t,u',

    'LEFT': 'v,w,x',
    'UP': 'y,z,f1',
    'RIGHT': 'f2,f3,f4',
    'DOWN': 'f5,f6,f7',

    'touch': 'f8,f9',

    'L1': 'f10',
    'R1': 'f11,f12',
    'R3': 'f13,f14',
    'L3': 'f15'
}


def get_angle(x, y):
    """
    Get the angle of the stick from the x and y axis values
    """
    return math.atan2(y, x) * 180 / math.pi


def get_stick_direction(x, y):
    """
    Get the direction of the stick from the x and y axis values
    """
    angle = get_angle(x, y)

    if -22.5 < angle < 22.5:
        return 'NE'
    elif 22.5 < angle < 67.5:
        return 'E'
    elif 67.5 < angle < 112.5:
        return 'SE'
    elif 112.5 < angle < 157.5:
        return 'S'
    elif -22.5 > angle > -67.5:
        return 'N'
    elif -67.5 > angle > -112.5:
        return 'NW'
    elif -112.5 > angle > -157.5:
        return 'W'
    elif angle > 157.5 or angle < -157.5:
        return 'SW'

    return None


def reset_mouse_to_center():
    w, h = pyautogui.size()
    x, y = pyautogui.position()
    if abs(x - w / 2) > 10 or abs(y - h / 2) > 10:
        pyautogui.mouseUp(button='right')
        pyautogui.moveTo(w / 2, h / 2)


def move_mouse_in_direction(direction, stick_amplitude):
    """
    Move the mouse in the given direction
    """
    large_offset = 300
    small_offset = 120
    offset = large_offset if stick_amplitude > 1 else small_offset

    w, h = pyautogui.size()
    cx, cy = w / 2, h / 2

    if direction == 'N':
        pyautogui.moveTo(cx + offset, cy - offset)
    elif direction == 'S':
        pyautogui.moveTo(cx - offset, cy + offset)
    elif direction == 'E':
        pyautogui.moveTo(cx + offset, cy + offset)
    elif direction == 'W':
        pyautogui.moveTo(cx - offset, cy - offset)
    elif direction == 'NE':
        pyautogui.moveTo(cx + offset, cy)
    elif direction == 'NW':
        pyautogui.moveTo(cx, cy - offset)
    elif direction == 'SE':
        pyautogui.moveTo(cx, cy + offset)
    elif direction == 'SW':
        pyautogui.moveTo(cx - offset, cy)
    pyautogui.mouseDown(button='right')


def get_button_alias_and_state(event):
    if event.dict['button'] == 4:
        return 'share', State.SHARE
    if event.dict['button'] == 6:
        return 'options', State.OPTIONS
    if event.dict['button'] == 7:
        return 'L3', State.L3
    if event.dict['button'] == 8:
        return 'R3', State.R3
    if event.dict['button'] == 15:
        return 'touch', State.TOUCH
    if event.dict['button'] == 2:
        return 'A', State.A
    if event.dict['button'] == 1:
        return 'D', State.D
    if event.dict['button'] == 0:
        return 'C', State.C
    if event.dict['button'] == 3:
        return 'B', State.B
    if event.dict['button'] == 9:
        return 'L1', State.L1
    if event.dict['button'] == 10:
        return 'R1', State.R1
    if event.dict['button'] == 11:
        return 'UP', State.UP
    if event.dict['button'] == 12:
        return 'DOWN', State.DOWN
    if event.dict['button'] == 13:
        return 'LEFT', State.LEFT
    if event.dict['button'] == 14:
        return 'RIGHT', State.RIGHT
    return 'None', State.NONE


class Stick:
    def __init__(self, dead_zone=0.5):
        self.dir = None
        self.prev_dir = None
        self.ampl = 0
        self.prev_ampl = 0
        self.dead_zone = dead_zone

    @staticmethod
    def get_direction(x, y):
        """
        Get the direction of the stick from the x and y axis values
        """
        angle = get_angle(x, y)

        if -22.5 < angle < 22.5:
            return 'NE'
        elif 22.5 < angle < 67.5:
            return 'E'
        elif 67.5 < angle < 112.5:
            return 'SE'
        elif 112.5 < angle < 157.5:
            return 'S'
        elif -22.5 > angle > -67.5:
            return 'N'
        elif -67.5 > angle > -112.5:
            return 'NW'
        elif -112.5 > angle > -157.5:
            return 'W'
        elif angle > 157.5 or angle < -157.5:
            return 'SW'

        return None


class LeftStick(Stick):

    def __init__(self, dead_zone=0.5):
        super().__init__(dead_zone)

    def update(self, x, y):
        self.dir = get_stick_direction(x, y)
        self.ampl = math.sqrt(x ** 2 + y ** 2)

        dir_changed = self.prev_dir != self.dir
        ampl_changed = abs(self.ampl - self.prev_ampl) > 0.1

        if not self.dir or self.ampl < self.dead_zone:
            reset_mouse_to_center()
            self.prev_dir = None
            self.prev_ampl = 0
        elif dir_changed or ampl_changed:
            angle = get_angle(x, y)
            print(f"Left stick angle: {angle} dir: {self.dir} ampl: {self.ampl}")
            move_mouse_in_direction(self.dir, self.ampl)
            self.prev_dir = self.dir
            self.prev_ampl = self.ampl


class RightStick(Stick):
    def __init__(self, key_maps, dead_zone=0.5):
        super().__init__(dead_zone)
        self.keys_down = set()
        self.key_maps = key_maps

    def get_stick_mapped_key(self, layer):
        """
        Returns mapped key for the given direction
        """
        km = self.key_maps[layer]
        if self.dir not in km:
            return None

        return km[self.dir]

    def update(self, x, y, layer):
        self.dir = get_stick_direction(x, y)
        self.ampl = math.sqrt(x ** 2 + y ** 2)
        dir_changed = self.dir != self.prev_dir

        if not self.dir or self.ampl < self.dead_zone:
            self.prev_dir = None
            for k in self.keys_down:
                ReleaseKey(k)
            self.keys_down.clear()
        elif dir_changed:
            print(f"Right stick: {self.dir}")
            self.prev_dir = self.dir
            k = self.get_stick_mapped_key(layer)
            if k and k not in self.keys_down:
                PressKey(k)
                self.keys_down.add(k)


class Trigger:
    def __init__(self, name, dead_zone=0.5):
        self.dead_zone = dead_zone
        self.name = name

    def is_down(self, value):
        if value > self.dead_zone:
            print(f"{self.name} is down, value: {value}")
            return True
        return False


class Layer(IntFlag):
    NONE = 0
    L2 = 1
    R2 = 2
    L2R2 = 3


class DS4Controller:
    def __init__(self):
        pygame.init()
        pygame.joystick.init()
        joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]

        if len(joysticks) == 0:
            print("No joysticks found")
            exit(1)

        self.key_maps = [{}, {}, {}, {}]

        self.pattern = re.compile(
            r'([a-zA-Z0-9_\[\]\-=().;:{}+]+)(?:,([a-zA-Z0-9_\[\]\-=().;:{}+]+),*)*([a-zA-Z0-9_\[\]\-=().;:{}+]+)*'
        )
        for k, v in KEY_MAP.items():
            m = self.pattern.match(v)
            if m:
                for i, g in enumerate(m.groups()):
                    if g:
                        self.key_maps[i][k] = g

        print(joysticks)
        self.joy = pygame.joystick.Joystick(0)
        self.joy.init()
        print(f"Name: {self.joy.get_name()}\nButtons: {self.joy.get_numbuttons()}\nAxes: {self.joy.get_numaxes()}\nBattery: {self.joy.get_power_level()}")

        self.left_stick = LeftStick()
        self.right_stick = RightStick(self.key_maps)
        self.left_trigger = Trigger('L2')
        self.right_trigger = Trigger('R2')

        self.button_state = State.NONE
        self.active = True

        self.layer = Layer.NONE

    def handle_button(self, alias, down=True):
        km = self.key_maps[self.layer]

        if alias not in km:
            print(f"No mapping for button: {alias}")
            return

        key = km[alias]
        print(f"BUTTON: {alias} -> {key}")
        if down:
            #pyautogui.keyDown(key)
            PressKey(key)
        else:
            # perform key up for all aliases of this button
            for jm in self.key_maps:
                if alias in jm:
                    #pyautogui.keyUp(jm[alias])
                    ReleaseKey(jm[alias])

    def update(self, pygame_events=None):

        if not pygame_events:
            pygame_events = []
        
        for event in pygame_events:
            if 'joy' in event.dict and event.dict['joy'] == self.joy.get_id():

                if self.active:
                    l2_is_down = self.left_trigger.is_down(self.joy.get_axis(4))
                    if l2_is_down:
                        self.layer = self.layer | Layer.L2
                        self.button_state = self.button_state | State.L2
                    else:
                        self.layer = self.layer & ~Layer.L2
                        self.button_state = self.button_state & ~State.L2

                    r2_is_down = self.right_trigger.is_down(self.joy.get_axis(5))
                    if r2_is_down:
                        self.layer = self.layer | Layer.R2
                        self.button_state = self.button_state | State.R2
                    else:
                        self.layer = self.layer & ~Layer.R2
                        self.button_state = self.button_state & ~State.R2

                    self.left_stick.update(self.joy.get_axis(0), self.joy.get_axis(1))
                    self.right_stick.update(self.joy.get_axis(2), self.joy.get_axis(3), self.layer)

                if event.type == BTN_DOWN:
                    alias, state = get_button_alias_and_state(event)
                    print(f"Button {alias} down")
                    self.button_state = self.button_state | state

                    if state & State.SHARE:
                        self.active = not self.active

                    if self.active:
                        self.handle_button(alias)
                elif event.type == BTN_UP and self.active:
                    alias, state = get_button_alias_and_state(event)
                    self.handle_button(alias, down=False)
                    print(f"Button {alias} up")
                    self.button_state = self.button_state & ~state

        return self.button_state if self.active else State.INACTIVE
    
    
if __name__ == '__main__':
    ds4 = DS4Controller()

    while True:
        ds4.update(pygame_events=pygame.event.get())
