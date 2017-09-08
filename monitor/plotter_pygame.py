from __future__ import division
import pygame
from pygame.locals import *
from epics import pv
import datetime
import sys

COLOUR_BLACK = (0, 0, 0)
COLOUR_WHITE = (255, 255, 255)
DEFAULT_COLORMAP = [Color(255-i, 255-i, 255-i) for i in range(256)]


class PyGamePlotter(object):

    def __init__(self, monitor, fullscreen):
        pygame.init()
        pygame.mouse.set_visible(False)
        pygame.display.set_caption(monitor)
        info = pygame.display.Info()

        # set screen size and mode (fullscreen, window border)
        if fullscreen:
            self._screen_size = (info.current_w, info.current_h)
            self._screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.NOFRAME)
        else:      
            self._screen_size = (600, 400)
            self._screen = pygame.display.set_mode(self._screen_size)

        
        # define font size as a function of screen size
        # font 50 looks good with 600 pixel wide... linear extrapolation from there
        self.font_size = int(self._screen_size[0] * 50.0 / 600.0)


        self._palette = DEFAULT_COLORMAP
        self._aspect = 0
        self._normalisation = 1
        self.name = "unset"

    def blank(self):
        self._screen.fill(COLOUR_BLACK)
        font = pygame.font.Font(None, self.font_size)
        text = font.render("No Camera Selected", 1, COLOUR_WHITE)
        textpos = text.get_rect()
        textpos.centerx = self._screen.get_rect().centerx
        textpos.centery = self._screen.get_rect().centery
        self._screen.blit(text, textpos)
        pygame.display.flip()

    def show_label(self, label):
        font = pygame.font.Font(None, self.font_size)
        text = font.render(label, 1, COLOUR_WHITE)
        self._screen.blit(text, (0, 0))

    def set_colormap(self, colormap):
        self._palette = [Color("0x" + colormap[i]) for i in range(256)]

    def set_name(self, name):
        self.name = name

    def _set_background(self, colour):
        background = pygame.Surface(self._screen_size)
        background.fill(colour)
        self._screen.blit(background, (0, 0))

    def set_aspect_ratio(self, aspect):
        self._aspect = aspect
          
    def set_normalisation(self, normalisation):
        self._normalisation = normalisation

    def _calc_size_pos(self, shape):
        """

        :param shape:
        :return: Return tuple (x, y, width, height)
        """
        # keeping aspect ratio
        if self._aspect == 1:

            dh = shape[1]
            dw = shape[0]
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

        return x, y, w, h

    def process(self, data):
        """ Data may be None if PV access fails
        :param data:
        :return:
        """
        if data is not None:

            # normalise data
            if self._normalisation == 1:
                maximum = data.max()
                if maximum>0: data = data * 255.0 / maximum

            # make surface from data
            surf = pygame.surfarray.make_surface(data)

            # set colourmap
            surf.set_palette(self._palette)

            # calculate dimension and position depending on aspect ratio
            (x, y, width, height) = self._calc_size_pos(data.shape)

            # rescale surface to appropriate dimension"
            surf = pygame.transform.scale(surf, (width, height))

            # set background colour
            self._set_background(COLOUR_BLACK)

            # plot surface to screen
            self._screen.blit(surf, (x, y))

    def show(self):
        pygame.display.flip()

    def close_requested(self):
        """ Check the pygame event queue for exit commands:
                - quit
                - Escape key-press

            :return:
                True if exit instruction detected
        """
        for event in pygame.event.get():
            if self.is_exit_event(event):
                return True

        return False

    @staticmethod
    def is_exit_event(event):
        """ Identify 'exit' events:
                - KEYDOWN + ESCAPE key
                - QUIT
            Returns:
                True if exit event
        """
        return ((event.type == KEYDOWN and event.key == K_ESCAPE)
                or event.type == pygame.QUIT)

    def quit(self):
        pygame.quit()
