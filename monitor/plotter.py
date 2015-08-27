#!/usr/bin/env dls-python
import matplotlib.pyplot as plt

class Plotter:

    def __init__(self):
        plt.ion()
        plt.axis('off')

    def set_image_size(self, xsize, ysize):
        pass

    def show(self, data):
        plt.imshow(data)

