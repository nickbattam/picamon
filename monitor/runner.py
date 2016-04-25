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
    plotter = PyGamePlotter(monitor)
    camera = Camera()
	
    old_cmap = ""
    old_timestamp = -1
    while True:
        try:

            # check for quit events
            if plotter.i_shall_continue()==False: break

            # get camera name, set blank screen if none
            camera_name = controller.camera
            if camera_name == "":
                plotter.blank()
                continue
 
            camera.set_name(camera_name)

            # update colormap
            cmap = controller.colourmap_name
            if cmap != old_cmap:
                old_cmap = cmap
                plotter.set_colormap(controller.colourmap_data)
                    
            # update aspect ratio
            plotter.set_aspect_ratio(controller.aspect)

            # update data
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

