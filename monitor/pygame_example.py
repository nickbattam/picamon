from pkg_resources import require
require("numpy")

import numpy as np
import sys
import pygame

width=500
height=500
size  = (width, height)
data = np.random.randint(0,100,size)
print data

pygame.init()
screen = pygame.display.set_mode(size)

while 1:
	for event in pygame.event.get():
		if event.type == pygame.QUIT: sys.exit(0)
		pygame.surfarray.blit_array(screen,data)
		pygame.display.flip()


