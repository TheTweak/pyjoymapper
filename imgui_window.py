import sys
import imgui
import pygame

import OpenGL.GL as gl
from imgui.integrations.pygame import PygameRenderer
from utils import State

COL_WIDTH = 70
BTN_WIDTH = COL_WIDTH
BTN_HEIGHT = 25


def new_lines(n):
    for _ in range(n):
        imgui.new_line()


def skip_columns(n):
    for _ in range(n):
        imgui.next_column()


def empty(n):
    for _ in range(n):
        imgui.invisible_button('', BTN_WIDTH, BTN_HEIGHT)


def button(text, pressed=False):
    if pressed:
        imgui.push_style_color(imgui.COLOR_BUTTON, 0, 0.5, 0, 1)

    imgui.button(text, BTN_WIDTH, BTN_HEIGHT)

    if pressed:
        imgui.pop_style_color()


class MainWindow:
    def __init__(self):
        self.size = (500, 200)
        self.window = pygame.display.set_mode(self.size, pygame.DOUBLEBUF | pygame.OPENGL)

        imgui.create_context()
        self.impl = PygameRenderer()

        io = imgui.get_io()
        io.display_size = self.size

    def render(self):
        gl.glClearColor(1, 1, 1, 1)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)
        imgui.render()
        self.impl.render(imgui.get_draw_data())
        pygame.display.flip()

    def update(self, button_state, pygame_events=None):
        if pygame_events is None:
            pygame_events = []

        for event in pygame_events:
            if event.type == pygame.QUIT:
                sys.exit()

            self.impl.process_event(event)

        imgui.new_frame()
        imgui.set_next_window_position(0, 0)
        imgui.set_next_window_size(self.size[0], self.size[1])
        imgui.begin("main", flags=imgui.WINDOW_NO_TITLE_BAR | imgui.WINDOW_NO_RESIZE | imgui.WINDOW_NO_MOVE)

        if button_state == State.INACTIVE:
            imgui.text('Press Share to start')
            imgui.end()
            self.render()
            return

        cols = 9
        imgui.columns(cols, 'buttons', False)
        for i in range(cols):
            imgui.set_column_width(i, COL_WIDTH)

        empty(4)
        button('left', button_state & State.LEFT)
        imgui.next_column()

        button('L2  ', button_state & State.L2)
        button('L1  ', button_state & State.L1)
        empty(1)
        button('up  ', button_state & State.UP)
        empty(1)
        button('down', button_state & State.DOWN)
        imgui.next_column()

        empty(2)
        button('share', button_state & State.SHARE)
        empty(1)
        button('right', button_state & State.RIGHT)
        imgui.next_column()

        empty(4)
        button('touch', button_state & State.TOUCH)
        imgui.next_column()

        empty(2)
        button('options', button_state & State.OPTIONS)
        empty(1)
        button('a', button_state & State.A)
        imgui.next_column()

        button('R2  ', button_state & State.R2)
        button('R1  ', button_state & State.R1)
        empty(1)
        button('b', button_state & State.B)
        empty(1)
        button('c', button_state & State.C)
        imgui.next_column()

        empty(4)
        button('d', button_state & State.D)

        imgui.columns(1)
        imgui.end()

        self.render()


if __name__ == '__main__':
    main_window = MainWindow()
    while 1:
        main_window.update(State.L2, pygame.event.get())
