import sys
from time import sleep
from camera import Camera
from controller import Controller
from plotter_pygame import PyGamePlotter
import epics
import argparse


class Monitor(object):

    def __init__(self, plotter, controller):
        self.plotter = plotter
        self.camera = Camera()
        self.controller = controller

    def start(self):

        old_cmap = ""
        while True:
            try:
                # check for quit events
                if plotter.close_requested():
                    break

                # get camera name
                camera.update_name(controller.camera)

                # if no camera is selected, make screen blank
                if not camera.has_feed():
                    plotter.blank()

                # otherwise, display camera feed
                else:

                    # update colormap
                    cmap = controller.colourmap_name
                    if cmap is not None and cmap != old_cmap:
                        data = controller.colourmap_data
                        if data is not None:
                            old_cmap = cmap
                            plotter.set_colormap(data)

                    # update aspect ratio
                    plotter.set_aspect_ratio(controller.aspect)

                    # get camera data and process it
                    plotter.process(camera.get_data())

                    # udpate label info
                    if controller.label == 1:
                        plotter.show_label(camera.name)
                        pass

                # show and wait
                plotter.show()
                sleep(controller.rate)

            except KeyboardInterrupt:
                plotter.quit()
                pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--prefix', required=True, dest='prefix', help='controller IOC prefix')
    parser.add_argument('--name', required=True, dest='name', help='name of monitor')
    parser.add_argument('--fullscreen', dest='fullscreen', type=bool, default=True, help='True for fullscreen (default), False for small window')
    args = parser.parse_args()

    controller = Controller(args.prefix, args.name)
    plotter = PyGamePlotter(args.name, args.fullscreen)
    monitor = Monitor(plotter, controller)

    monitor.start()
    plotter.quit()

