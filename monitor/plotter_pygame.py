from __future__ import division
import pygame
from pygame.locals import *
from epics import pv


DEFAULT_COLORMAP = [Color(255-i,255-i,255-i) for i in range(256)]

class PyGamePlotter(object):


    def __init__(self, monitor):
        pygame.init()
        pygame.mouse.set_visible(False)
        pygame.display.set_caption(monitor)

        info = pygame.display.Info()
        self._screen_size = (600,400)
        #self._screen_size = (info.current_w,info.current_h)


        self._screen = pygame.display.set_mode(self._screen_size)
        #self._screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN|pygame.NOFRAME)

        self._palette = DEFAULT_COLORMAP
        self._background = (0,0,0)
        self._aspect = 0

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
        self._palette = [Color("0x" + colormap[i]) for i in range(256)]


    def set_name(self, name):
        self.name = name


    def set_aspect_ratio(self, aspect):

        if self._aspect != aspect:
            self._aspect = aspect

            # blit the screen with background colour
            background = pygame.Surface(self._screen_size)
            background.fill(self._background)
            self._screen.blit(background,(0,0)) 


    def show(self, data):
        try:
            surf = pygame.surfarray.make_surface(data)
            surf.set_palette(self._palette)

            # keeping aspect ratio
            if self._aspect == 1:

                dh = data.shape[0]
                dw = data.shape[1]
                da = dw/dh

                sw = self._screen_size[0]
                sh = self._screen_size[1]
                sa =  sw / sh
                
                if  da < sa:
                    scale_w = sh / dh
                    h = sh
                    w = int( dw * scale_w )
                    x = int( 0.5 * ( sw - w ) )
                    y = 0           
                else:
                    scale_h = sw / dw
                    w = sw
                    h = int( dh * scale_h )
                    x = 0
                    y = int( 0.5 * ( sh - h) )

            # stretching to fullscreen
            elif self._aspect == 0:
                
                x = y = 0
                w = self._screen_size[0]
                h = self._screen_size[1]

            else:
                pass #todo log errors?

            surf = pygame.transform.scale(surf,(w,h))
            self._screen.blit(surf,(x,y)) 
            pygame.display.flip()

        except:
            pass


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
