import epics

CA_TIMEOUT = 5  # sec


class Controller(object):

    def __init__(self, prefix, monitor):
        self._prefix = prefix

        self.camera_pv = epics.PV("{0}:{1}:CAMERA".format(prefix, monitor))
        self.rate_pv = epics.PV("{0}:{1}:RATE".format(prefix, monitor))
        self.colourmap_pv = epics.PV("{0}:{1}:COLORMAP".format(prefix, monitor))
        self.aspect_pv = epics.PV("{0}:{1}:ASPECT".format(prefix, monitor))
        self.label_pv = epics.PV("{0}:{1}:LABEL".format(prefix, monitor))
        self.normalisation_pv = epics.PV("{0}:{1}:NORMALISATION".format(prefix, monitor))

        self.monitor_list_pv = epics.PV("{0}:LIST:MONITOR".format(prefix))
        _ = self.monitor_list_pv.get()

        self.camera_list_pv = epics.PV("{0}:LIST:CAMERA".format(prefix))
        _ = self.camera_list_pv.get()

        self.colormap_list_pv = epics.PV("{0}:LIST:COLORMAP".format(prefix))
        _ = self.colormap_list_pv.get()

    def close(self):
        self.camera_pv.disconnect()
        self.rate_pv.disconnect()
        self.colourmap_pv.disconnect()
        self.aspect_pv.disconnect()
        self.label_pv.disconnect()
        self.normalisation_pv.disconnect()

    @property
    def camera(self):
        camera = self.camera_pv.get()
        cameras = self.camera_list_pv.get()
        if cameras is not None and camera in cameras:
            return camera
        else:
            return ""

    @property
    def rate(self):
        return self.rate_pv.get()

    @property
    def aspect(self):
        return self.aspect_pv.get()

    @property
    def label(self):
        return self.label_pv.get()

    @property
    def normalisation(self):
        return self.normalisation_pv.get()

    @property
    def colourmap_name(self):
        colormap = self.colourmap_pv.get()
        colormaps = self.colormap_list_pv.get()
        return colormap if colormap in colormaps else None

    @property
    def colourmap_data(self):
        """ Get the colour map, this is an array

        :return: PV value or NONE if request timesout or
            colourmap name unset
        """
        colourmap = None
        if self.colourmap_name is not None:
            pv_name = self._prefix + ":CMAP:" + str(self.colourmap_name).upper()
            colourmap = epics.caget(pv_name, timeout=CA_TIMEOUT)
        return colourmap
