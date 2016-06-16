from __future__ import division
import pygame
from pygame.locals import *
from epics import pv
import datetime
import sys

DEFAULT_COLORMAP = [Color(255-i, 255-i, 255-i) for i in range(256)]


class PyGamePlotter(object):

    def __init__(self, monitor, fullscreen):
        pygame.init()
        pygame.mouse.set_visible(False)
        pygame.display.set_caption(monitor)

        info = pygame.display.Info()

        if fullscreen == 1:
            self._screen_size = (info.current_w,info.current_h)
            self._screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN|pygame.NOFRAME)
        else:      
            self._screen_size = (600,400)
            self._screen = pygame.display.set_mode(self._screen_size)

        self._palette = DEFAULT_COLORMAP
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

    def show_label(self, label):
        font = pygame.font.Font(None, 50)
        text = font.render(label, 1,(255,255,255))
        self._screen.blit(text,(0,0))      

    def set_colormap(self, colormap):
        self._palette = [Color("0x" + colormap[i]) for i in range(256)]

    def set_name(self, name):
        self.name = name

    def _set_background(self, colour):
        background = pygame.Surface(self._screen_size)
        background.fill(colour)
        self._screen.blit(background,(0,0)) 

    def set_aspect_ratio(self, aspect):
        self._aspect = aspect
          
    def _calc_size_pos(self, shape):
            
        # keeping aspect ratio
        if self._aspect == 1:

            dh = shape[0]
            dw = shape[1]
            da = dw/dh

            sw = self._screen_size[0]
            sh = self._screen_size[1]
            sa = sw / sh
            
            if da < sa:
                scale_w = sh / dh
                h = sh
                w = int(dw * scale_w)
                x = int(0.5 * (sw - w))
                y = 0           
            else:
                scale_h = sw / dw
                w = sw
                h = int(dh * scale_h)
                x = 0
                y = int(0.5 * (sh - h))

        # stretching to fullscreen
        else:
            x = y = 0
            w = self._screen_size[0]
            h = self._screen_size[1]

        return (x, y, w, h)

    def process(self, data):

        # make surface from data
        surf = pygame.surfarray.make_surface(data)

        # set colourmap
        surf.set_palette(self._palette)

        # calculate dimension an position depending on aspect ratio
        size_pos = self._calc_size_pos(data.shape)

        # rescale surface to appropriate dimension"
        surf = pygame.transform.scale(surf,(size_pos[2],size_pos[3]))

        # set background colour
        self._set_background((0,0,0))

        # plot surface to screen
        self._screen.blit(surf,(size_pos[0],size_pos[1]))

    def show(self):
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
