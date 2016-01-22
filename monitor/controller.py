from epics import pv

class Controller(object):
    """ Class that reads PVs from the EPICS IOC controller
    """

    def __init__(self, prefix, monitor):
        self.camera_pv = pv.PV(prefix + ":" + monitor + ":CAMERA")
        self.rate_pv = pv.PV(prefix + ":" + monitor + ":RATE")

    def close(self):
        self.camera_pv.disconnect()
        self.rate_pv.disconnect()

    @property
    def camera(self):
        return self.camera_pv.get()

    @property
    def rate(self):
        return self.rate_pv.get()

