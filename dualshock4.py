import pygame
import os

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

    while True:
        for event in pygame.event.get():
            if 'joy' in event.dict and event.dict['joy'] == joy.get_id():
                if event.type == BTN_DOWN:
                    print(f"Button {event.dict['button']} down")
                elif event.type == BTN_UP:
                    print(f"Button {event.dict['button']} up")
                elif event.type == AXIS_MOTION and abs(event.dict['value']) > AXIS_ACTIVATION_THRESHOLD:
                    print(f"Axis {event.dict['axis']} moved to {event.dict['value']}")