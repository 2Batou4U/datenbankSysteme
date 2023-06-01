import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *


def init():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -5)


def draw_cube():
    vertices = (
        (1, 1, 1),
        (1, 1, -1),
        (1, -1, 1),
        (1, -1, -1),
        (-1, 1, 1),
        (-1, 1, -1),
        (-1, -1, -1),
        (-1, -1, 1)
    )

    edges = (
        (0, 1),
        (0, 2),
        (0, 4),
        (1, 5),
        (1, 3),
        (2, 3),
        (2, 7),
        (3, 6),
        (4, 7),
        (4, 5),
        (5, 6),
        (6, 7),
    )

    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()


def game_loop():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        glRotatef(1, 3, 1, 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        draw_cube()
        pygame.display.flip()
        pygame.time.wait(10)


def main():
    init()
    game_loop()


if __name__ == '__main__':
    main()
