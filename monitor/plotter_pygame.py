import pygame
from pygame.locals import *

DEFAULT_XSIZE = 500
DEFAULT_YSIZE = 500

class PyGamePlotter(object):

    def __init__(self):
        pygame.init()
	pygame.mouse.set_visible(False)
        self._screen_size = (DEFAULT_XSIZE, DEFAULT_YSIZE)
        #self._screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN|pygame.NOFRAME)
        self._screen = pygame.display.set_mode(self._screen_size)

    def set_screensize(self, xsize, ysize):
        screen_size = (xsize, ysize)
        if screen_size != self._screen_size:
            #self._screen = pygame.display.set_mode(screen_size, pygame.FULLSCREEN)
            self._screen = pygame.display.set_mode(screen_size)

    def blank(self):
        self._screen.fill((0,0,0))

        font = pygame.font.Font(None, 50)
        text = font.render("No Camera Selected",1,(255,255,255))
        textpos = text.get_rect()
        textpos.centerx = self._screen.get_rect().centerx
        textpos.centery = self._screen.get_rect().centery
        self._screen.blit(text, textpos)

        pygame.display.flip()

    def show(self, data):
        pygame.surfarray.blit_array(self._screen, data)
        pygame.display.flip()


    def i_shall_continue(self):
        for event in pygame.event.get():
             if event.type == pygame.QUIT:
                 return False
	     elif event.type == KEYDOWN and event.key==K_ESCAPE:
                 return False
             else:
                 return True

    def quit(self):
        pygame.quit()
