import time
import os
import pygame

from keypress import press_key, key_down, key_up

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
AXIS_ACTIVATION_THRESHOLD = 0.7
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
AXIS_TO_DIR_EPS = 0.1
RIGHT_STICK_UPDATE_INTERVAL_MSEC = 200
LEFT_STICK_UPDATE_INTERVAL_MSEC = 1
KEY_MAP = {
    'LEFT_STICK': {
        'S': 'z',
        'N': 'e',
        'W': 'q',
        'E': 'c',
        'SW': 'a',
        'SE': 'x',
        'NE': 'd',
        'NW': 'w'
    }
}


def get_stick_direction(x, y):
    """
    Get the direction of the stick from the x and y axis values
    """
    if x > 0.6 and y > 0.6:
        return 'E'
    elif x < -0.6 and y < -0.6:
        return 'W'
    elif x > 0.6 and y < -0.6:
        return 'N'
    elif x < -0.6 and y > 0.6:
        return 'S'
    elif x > 0.6:
        return 'NE'
    elif x < -0.6:
        return 'SW'
    elif y > 0.6:
        return 'SE'
    elif y < -0.6:
        return 'NW'

    return None


def get_stick_mapped_key(stick, direction):
    """
    Returns mapped key for the given stick and direction
    """
    if stick not in KEY_MAP or direction not in KEY_MAP[stick]:
        return None

    return KEY_MAP[stick][direction]


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
    keys_down = set()
    while True:
        for event in pygame.event.get():
            if 'joy' in event.dict and event.dict['joy'] == joy.get_id():

                if event.type == BTN_DOWN:
                    print(f"Button {event.dict['button']} down")
                elif event.type == BTN_UP:
                    print(f"Button {event.dict['button']} up")
                else:
                    left_stick_dir = get_stick_direction(joy.get_axis(0), joy.get_axis(1))
                    if left_stick_dir:
                        print(f'Left stick: {left_stick_dir} {event}')
                        k = get_stick_mapped_key('LEFT_STICK', left_stick_dir)
                        if k not in keys_down:
                            key_down(k)
                            keys_down.add(k)
                    else:
                        for k in keys_down:
                            key_up(k)
                        keys_down.clear()
