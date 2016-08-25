import epics

CA_TIMEOUT = 5  # sec


class Controller(object):
    """ Class that reads PVs from the EPICS IOC controller
    """

    def __init__(self, prefix, monitor):
        self.prefix = prefix
        self.monitor = monitor
        self.camera_pv = epics.PV(prefix + ":" + monitor + ":CAMERA")
        self.rate_pv = epics.PV(prefix + ":" + monitor + ":RATE")
        self.colourmap_pv = epics.PV(prefix + ":" + monitor + ":COLORMAP")
        self.aspect_pv = epics.PV(prefix + ":" + monitor + ":ASPECT")
        self.label_pv = epics.PV(prefix + ":" + monitor + ":LABEL")

    def close(self):
        self.camera_pv.disconnect()
        self.rate_pv.disconnect()
        self.colourmap_pv.disconnect()
        self.aspect_pv.disconnect()
        self.label_pv.disconnect()

    @property
    def camera(self): return self.camera_pv.get()

    @property
    def rate(self): return self.rate_pv.get()

    @property
    def aspect(self): return self.aspect_pv.get()

    @property
    def label(self): return self.label_pv.get()

    @property
    def colourmap_name(self):
        return self.colourmap_pv.get()

    @property
    def colourmap_data(self):
        """ Get the colour map, this is an array

        :return: PV value or NONE if request timesout
        """
        pv_name = self.prefix + ":CMAP:" + str(self.colourmap_name).upper()
        return epics.caget(pv_name, timeout=CA_TIMEOUT)
