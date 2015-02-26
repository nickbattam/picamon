#!/usr/bin/env dls-python
import matplotlib.pyplot as plt

class Plotter:

    def __init__(self):
        plt.ion()
        plt.axis('off')

    def show(data,xsize,ysize):
        plt.show(data)