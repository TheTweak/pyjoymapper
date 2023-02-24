import sys
import imgui
import pygame

import OpenGL.GL as gl
from imgui.integrations.pygame import PygameRenderer


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


def button(text):
    imgui.button(text, BTN_WIDTH, BTN_HEIGHT)


if __name__ == '__main__':
    pygame.init()
    size = (500, 200)

    pygame.display.set_mode(size, pygame.DOUBLEBUF | pygame.OPENGL)

    imgui.create_context()
    impl = PygameRenderer()

    io = imgui.get_io()
    io.display_size = size

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            impl.process_event(event)

        imgui.new_frame()
        imgui.set_next_window_position(0, 0)
        imgui.set_next_window_size(size[0], size[1])
        imgui.begin("main", flags=imgui.WINDOW_NO_TITLE_BAR | imgui.WINDOW_NO_RESIZE | imgui.WINDOW_NO_MOVE)

        cols = 9
        imgui.columns(cols, 'buttons', False)
        for i in range(cols):
            imgui.set_column_width(i, COL_WIDTH)

        empty(4)
        button('left')
        imgui.next_column()

        button('L2  ')
        button('L1  ')        
        empty(1)
        button('up  ')
        empty(1)
        button('down')
        imgui.next_column()

        empty(2)
        button('share')
        empty(1)
        button('right')
        imgui.next_column()

        empty(4)
        button('touch')
        imgui.next_column()

        empty(2)
        button('options')
        empty(1)
        button('a')
        imgui.next_column()

        button('R2  ')
        button('R1  ')
        empty(1)
        button('b')
        empty(1)
        button('c')
        imgui.next_column()

        empty(4)
        button('d')

        imgui.columns(1)
        imgui.end()

        gl.glClearColor(1, 1, 1, 1)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)
        imgui.render()
        impl.render(imgui.get_draw_data())

        pygame.display.flip()