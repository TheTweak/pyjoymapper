from dualshock4 import DS4Controller
from imgui_window import MainWindow
import pygame

if __name__ == '__main__':
    controller = DS4Controller()
    main_window = MainWindow()

    while True:
        events = pygame.event.get()
        button_state = controller.update(events)
        main_window.update(button_state, events)
