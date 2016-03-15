from epics import pv

class Controller(object):
    """ Class that reads PVs from the EPICS IOC controller
    """

    def __init__(self, prefix, monitor):
        self.prefix = prefix
        self.monitor = monitor
        self.camera_pv = pv.PV(prefix + ":" + monitor + ":CAMERA")
        self.rate_pv = pv.PV(prefix + ":" + monitor + ":RATE")
        self.colourmap_pv = pv.PV(prefix + ":" + monitor + ":COLORMAP")
        self.aspect_pv = pv.PV(prefix + ":" + monitor + ":ASPECT")
        self.label_pv = pv.PV(prefix + ":" + monitor + ":LABEL")

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
        cmap_name = self.colourmap_name
        cmap_pv = pv.PV(self.prefix + ":CMAP:" + str(cmap_name).upper())
        data = cmap_pv.get()
        cmap_pv.disconnect()
        return data
        

