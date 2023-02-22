import os
import math
import pyautogui
import pygame

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
    'RIGHT_STICK': {
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


def get_stick_mapped_key(stick, direction):
    """
    Returns mapped key for the given stick and direction
    """
    if stick not in KEY_MAP or direction not in KEY_MAP[stick]:
        return None

    return KEY_MAP[stick][direction]


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

    keys_down = set()
    prev_left_stick_dir = None
    prev_right_stick_dir = None
    prev_left_stick_ampl = 0
    reset_mouse_to_center()

    while True:
        for event in pygame.event.get():
            if 'joy' in event.dict and event.dict['joy'] == joy.get_id():

                if event.type == BTN_DOWN:
                    print(f"Button {event.dict['button']} down")
                elif event.type == BTN_UP:
                    print(f"Button {event.dict['button']} up")
                else:
                    left_stick_dir = get_stick_direction(joy.get_axis(0), joy.get_axis(1))
                    amplitude = math.sqrt(joy.get_axis(0) ** 2 + joy.get_axis(1) ** 2)
                    dead_zone = 0.5
                    dir_changed = prev_left_stick_dir != left_stick_dir
                    ampl_changed = abs(prev_left_stick_ampl - amplitude) > 0.1

                    if not left_stick_dir or amplitude < dead_zone:
                        reset_mouse_to_center()
                        prev_left_stick_dir = None
                        prev_left_stick_ampl = 0
                    elif dir_changed or ampl_changed:
                        angle = get_angle(joy.get_axis(0), joy.get_axis(1))
                        print(f"Left stick angle: {angle} dir: {left_stick_dir} ampl: {amplitude}")
                        move_mouse_in_direction(left_stick_dir, amplitude)
                        prev_left_stick_dir = left_stick_dir
                        prev_left_stick_ampl = amplitude

                    right_stick_dir = get_stick_direction(joy.get_axis(2), joy.get_axis(3))
                    right_amplitude = math.sqrt(joy.get_axis(2) ** 2 + joy.get_axis(3) ** 2)
                    right_dir_changed = prev_right_stick_dir != right_stick_dir

                    if not right_stick_dir or right_amplitude < dead_zone:
                        prev_right_stick_dir = None
                        for k in keys_down:
                            pyautogui.keyUp(k)
                        keys_down.clear()
                    elif right_dir_changed:
                        print(f"Right stick: {right_stick_dir}")
                        prev_right_stick_dir = right_stick_dir
                        k = get_stick_mapped_key('RIGHT_STICK', right_stick_dir)
                        if k not in keys_down:
                            pyautogui.keyDown(k)
                            keys_down.add(k)
