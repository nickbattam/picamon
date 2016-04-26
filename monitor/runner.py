import sys
from time import sleep
from camera import Camera
from controller import Controller
from plotter_pygame import PyGamePlotter
import epics
import argparse

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--prefix', dest='prefix', help='controller IOC prefix')
    parser.add_argument('--name', dest='name', help='name of monitor')
    parser.add_argument('--fullscreen', dest='fullscreen', default=1, help='1 for fullscreen (default), 0 for small window')
    args = parser.parse_args()

    if not (args.prefix and args.name):
        parser.error("Arguments missing. Please use both --prefix and --name")

    controller = Controller(args.prefix, args.name)
    plotter = PyGamePlotter(args.name, args.fullscreen)
    camera = Camera()
	
    old_cmap = ""
    while True:
        try:

            # check for quit events
            if plotter.i_shall_continue() == False: break

            # get camera name
            camera_name = controller.camera

            # if no camera is selected, make screen blank
            if camera_name == "":
                plotter.blank()

            # otherwise, display camera feed
            else:

                camera.set_name(camera_name)

                # update colormap
                cmap = controller.colourmap_name
                if cmap != old_cmap:
                    old_cmap = cmap
                    plotter.set_colormap(controller.colourmap_data)
                        
                # update aspect ratio
                plotter.set_aspect_ratio(controller.aspect)

                # get camera data and process it
                plotter.process(camera.get_data())

                # udpate label info
                if controller.label==1:
                    plotter.show_label(camera_name)     
                    pass         

            # show and wait
            plotter.show()
            sleep(controller.rate)

        except KeyboardInterrupt:            
            plotter.quit()
            pass

    plotter.quit()

