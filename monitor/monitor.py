from time import sleep
from camera import Camera


class Monitor(object):

    def __init__(self, plotter, controller):
        self.plotter = plotter
        self.camera = Camera()
        self.controller = controller
        self.colourmap = ""

    def update_colourmap(self, old_colourmap):
        colourmap = self.controller.colourmap_name
        if colourmap is not None and colourmap != old_colourmap and colourmap is not "":
            data = self.controller.colourmap_data
            if data is not None:
                self.plotter.set_colormap(data)
                self.colourmap = colourmap

    def start(self):
        while True:
            try:
                # check for quit events
                if self.plotter.close_requested():
                    break

                # get camera name
                self.camera.update_name(self.controller.camera)

                # if no camera is selected, make screen blank
                if not self.camera.has_feed():
                    self.plotter.blank()

                # otherwise, display camera feed
                else:
                    # update colormap
                    self.update_colourmap(self.colourmap) 

                    # update aspect ratio
                    self.plotter.set_aspect_ratio(self.controller.aspect)

                    # update normalisation
                    self.plotter.set_normalisation(self.controller.normalisation)

                    # get camera data and process it
                    self.plotter.process(self.camera.get_data())

                    # update label info
                    if self.controller.label == 1:
                        self.plotter.show_label(self.camera.name)
                        pass

                # show and wait
                self.plotter.show()
                sleep(self.controller.rate)

            except KeyboardInterrupt:
                self.plotter.quit()
