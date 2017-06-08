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

        self.monitor_list_pv = epics.PV("{0}:LIST:MONITOR".format(prefix))

        self.camera_pv = epics.PV("{0}:{1}:CAMERA".format(prefix, monitor))
        self.rate_pv = epics.PV("{0}:{1}:RATE".format(prefix, monitor))
        self.colourmap_pv = epics.PV("{0}:{1}:COLORMAP".format(prefix, monitor))
        self.aspect_pv = epics.PV("{0}:{1}:ASPECT".format(prefix, monitor))
        self.label_pv = epics.PV("{0}:{1}:LABEL".format(prefix, monitor))

        # check the connection here; this is the simplest way to verify that
        # the named IOC exists
        if not self.monitor_list_pv.wait_for_connection(1.0):
            raise ValueError("Failed to connect to controller IOC: {0}".format(prefix))

        monitors = self.monitor_list_pv.get()
        if monitors is None:
            raise ValueError("No data returned from IOC: {0}".format(prefix))
        elif monitor not in monitors:
            raise ValueError("Specified monitor ({0}) is not defined in controller IOC ({0})".format(monitor, prefix))

    def close(self):
        self.camera_pv.disconnect()
        self.rate_pv.disconnect()
        self.colourmap_pv.disconnect()
        self.aspect_pv.disconnect()
        self.label_pv.disconnect()

    @property
    def camera(self):
        camera_name = self.camera_pv.get()
        # if camera_name not in self.camera_name_lists:
        #     TODO: handle camera names
        #     print camera_name
        #     raise ValueError()

        return camera_name

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
        return self.colourmap_pv.get()

    @property
    def colourmap_data(self):
        """ Get the colour map, this is an array

        :return: PV value or NONE if request timesout
        """
        pv_name = self._prefix + ":CMAP:" + str(self.colourmap_name).upper()
        return epics.caget(pv_name, timeout=CA_TIMEOUT)
