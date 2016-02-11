import sys
from time import sleep
from camera import Camera
from controller import Controller
from plotter_pygame import PyGamePlotter
import epics

if __name__ == "__main__":

    prefix = "MON-CONTROL"
    monitor = sys.argv[1]

    controller = Controller(prefix, monitor)

    plotter = PyGamePlotter()
	
    old_timestamp = -1
    while True:
        try:

            # check for quit events
            if plotter.i_shall_continue()==False: break

            # get camera name, set blank screen if none
            camera_name = controller.camera
            if not camera_name:
                plotter.blank()
                sleep(0.1)
                continue
            camera = Camera(camera_name)

            # update colormap
            #plotter.set_colormap("something")

            # update data
            data, timestamp = camera.get_image_data()
            if timestamp != old_timestamp:
                plotter.show(data)
                old_timestamp = timestamp

            sleep(controller.rate)

        except KeyboardInterrupt:
            if camera: camera.close()
            plotter.quit()

    plotter.quit()
