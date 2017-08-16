import epics

CA_TIMEOUT = 5  # sec


class Controller(object):
    """ Class that reads PVs from the EPICS IOC controller
    """

    def __init__(self, prefix, monitor):
        """ Create an instance of the controller for a single
            monitor.

            The monitor must be configured in the Controller database

            prefix: Controller IOC name
            monitor: name of the camera instance
        """
        self._prefix = prefix

        self.camera_pv = epics.PV("{0}:{1}:CAMERA".format(prefix, monitor))
        self.rate_pv = epics.PV("{0}:{1}:RATE".format(prefix, monitor))
        self.colourmap_pv = epics.PV("{0}:{1}:COLORMAP".format(prefix, monitor))
        self.aspect_pv = epics.PV("{0}:{1}:ASPECT".format(prefix, monitor))
        self.label_pv = epics.PV("{0}:{1}:LABEL".format(prefix, monitor))

        # check the connection here; this is the simplest way to verify that
        # the named IOC exists
        if not self.camera_pv.wait_for_connection(1.0):
            raise ValueError("Failed to connect to controller IOC: {0}".format(prefix))

        # check there is list of "registered" monitors to use
        self.monitor_list_pv = epics.PV("{0}:LIST:MONITOR".format(prefix))
        monitors = self.monitor_list_pv.get()
        if monitors is None:
            raise ValueError("No monitors registered with controller: {0}".format(prefix))
        
        # check that the specified monitor exists!
        if monitor not in monitors:
            raise ValueError("Specified monitor ({0}) is not defined in controller IOC ({0})".format(monitor, prefix))


        # check there is list of "registered" cameras to use
        self.camera_list_pv = epics.PV("{0}:LIST:CAMERA".format(prefix))
        cameras = self.camera_list_pv.get()
        if cameras is None:
            raise ValueError("No cameras registered with controller: {0}".format(prefix))


        # check there is list of "registered" colormaps to use
        self.colormap_list_pv = epics.PV("{0}:LIST:COLORMAP".format(prefix))
        colormaps = self.colormap_list_pv.get()
        if colormaps is None:
            raise ValueError("No colormaps registered with controller: {0}".format(prefix))


    def close(self):
        self.camera_pv.disconnect()
        self.rate_pv.disconnect()
        self.colourmap_pv.disconnect()
        self.aspect_pv.disconnect()
        self.label_pv.disconnect()

    @property
    def camera(self):
        camera = self.camera_pv.get()
        cameras = self.camera_list_pv.get()
        return camera if camera in cameras else ""


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
    def colourmap_name(self):
        colormap = self.colourmap_pv.get()
        colormaps = self.colormap_list_pv.get()
        return colormap if colormap in colormaps else None

    @property
    def colourmap_data(self):
        """ Get the colour map, this is an array

        :return: PV value or NONE if request timesout
        """
        pv_name = self._prefix + ":CMAP:" + str(self.colourmap_name).upper()
        return epics.caget(pv_name, timeout=CA_TIMEOUT)

