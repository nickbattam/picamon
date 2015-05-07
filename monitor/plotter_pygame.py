import pygame

DEFAULT_XSIZE = 500
DEFAULT_YSIZE = 500


class PyGamePlotter(object):

    def __init__(self):
        pygame.init()

        self._screen_size = (DEFAULT_XSIZE, DEFAULT_YSIZE)
        self._screen = pygame.display.set_mode(self._screen_size)

    def set_screensize(self, xsize, ysize):
        screen_size = (xsize, ysize)
        if screen_size != self._screen_size:
            self._screen = pygame.display.set_mode(screen_size)

    def show(self, data):
        pygame.surfarray.blit_array(self._screen, data)
        pygame.display.flip()





