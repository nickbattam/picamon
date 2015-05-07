from time import sleep

__author__ = 'nick'


def run(plotter, camera):

    while(1):
        plotter.show(camera.get_image_data())
        sleep(1.0)