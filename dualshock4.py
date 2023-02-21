import time
import os
import pygame

from keypress import press_key

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
AXIS_ACTIVATION_THRESHOLD = 0.1
AXIS_TO_DIR = {
    (-1,  1): 'S',
    (1,  -1): 'N',
    (-1, -1): 'W',
    (1,   1): 'E',
    (-1,  0): 'SW',
    (0,   1): 'SE',
    (1,   0): 'NE',
    (0,  -1): 'NW'
}
AXIS_TO_DIR_EPS = 0.4
RIGHT_STICK_UPDATE_INTERVAL_MSEC = 200
LEFT_STICK_UPDATE_INTERVAL_MSEC = 100
KEY_MAP = {
    'LEFT_STICK': {
        'S': 'control_z',
        'N': 'control_e',
        'W': 'control_q',
        'E': 'control_c',
        'SW': 'control_a',
        'SE': 'control_x',
        'NE': 'control_d',
        'NW': 'control_w'
    }
}


def get_stick_direction(x, y):
    """
    Get the direction of the stick from the x and y axis values
    """
    for k, v in AXIS_TO_DIR.items():
        if abs(x - k[0]) < AXIS_TO_DIR_EPS and abs(y - k[1]) < AXIS_TO_DIR_EPS:
            return v
    return None


def stick_mapped_key(stick, direction):
    """
    Press the mapped key for the given stick and direction
    """
    if stick not in KEY_MAP or direction not in KEY_MAP[stick]:
        return

    modifier, key = KEY_MAP[stick][direction].split('_')
    press_key(key, modifier=modifier)


if __name__ == '__main__':
    pygame.init()
    pygame.joystick.init()
    joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]

    if len(joysticks) == 0:
        print("No joysticks found")
        exit(1)

    print(joysticks)
    joy = pygame.joystick.Joystick(0)
    joy.init()
    print(f"Name: {joy.get_name()} | Buttons: {joy.get_numbuttons()} | Axes: {joy.get_numaxes()}")

    right_stick_update_time = 0
    left_stick_update_time = 0
    while True:
        for event in pygame.event.get():
            if 'joy' in event.dict and event.dict['joy'] == joy.get_id():

                if event.type == BTN_DOWN:
                    print(f"Button {event.dict['button']} down")
                elif event.type == BTN_UP:
                    print(f"Button {event.dict['button']} up")

                now = time.time() * 1000
                if now - left_stick_update_time > LEFT_STICK_UPDATE_INTERVAL_MSEC:
                    left_stick_update_time = now
                    left_stick_dir = get_stick_direction(joy.get_axis(0), joy.get_axis(1))
                    if left_stick_dir:
                        print(f'Left stick: {left_stick_dir}')
                        stick_mapped_key('LEFT_STICK', left_stick_dir)

                if now - right_stick_update_time > RIGHT_STICK_UPDATE_INTERVAL_MSEC:
                    right_stick_update_time = now
                    right_stick_dir = get_stick_direction(joy.get_axis(2), joy.get_axis(3))
                    if right_stick_dir:
                        print(f'Right stick: {right_stick_dir}')
