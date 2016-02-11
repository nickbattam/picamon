import pygame
from pygame.locals import *

DEFAULT_COLORMAP = [Color(i,i,i) for i in range(256)]

class PyGamePlotter(object):

    def __init__(self):
        pygame.init()
	pygame.mouse.set_visible(False)
        self._screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN|pygame.NOFRAME)

	info = pygame.display.Info()
	self._screen_size = (info.current_w,info.current_h)

	self._palette = DEFAULT_COLORMAP

    def blank(self):
        self._screen.fill((0,0,0))

        font = pygame.font.Font(None, 50)
        text = font.render("No Camera Selected",1,(255,255,255))
        textpos = text.get_rect()
        textpos.centerx = self._screen.get_rect().centerx
        textpos.centery = self._screen.get_rect().centery
        self._screen.blit(text, textpos)

        pygame.display.flip()


    def set_colormap(self,colormap):
	self._palette = [Color(i,i,255-i) for i in range(256)]


    def show(self, data):
        surf = pygame.surfarray.make_surface(data)
        surf.set_palette(self._palette)
	surf = pygame.transform.scale(surf,self._screen_size)
        self._screen.blit(surf, (0,0)) 
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
