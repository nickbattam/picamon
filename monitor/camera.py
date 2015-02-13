
from epics import pv


class Camera(object):
    """ Camera object for display. This wraps an instance of an EPICS 'camera'
        providing image data over CA.

        API decision need to be taken:
        - should the owning object be notified on updates to the data PV
          or do we depend the the owner polling at some controlled rate?
    """

    def __init__(self, prefix):
        """ Create a camera instance attached to a camera IOC
            supplying $(prefix):arrayData, $(prefix):xsize and
            $(prefix):ysize PVs
        """
        self.data_pv = pv.PV(prefix + ":arrayData")
        self.xsize_pv = pv.PV(prefix + ":xsize")
        self.ysize_pv = pv.PV(prefix + ":ysize")

    def close(self):
        """ Close camerate instance, disconnecting monitors and
            callback handlers
        """
        self.data_pv.disconnect()
        self.xsize_pv.disconnect()
        self.ysize_pv.diconnect()

    @property
    def xsize(self):
        return self.xsize_pv.get()

    @property
    def ysize(self):
        return self.ysize_pv.get()

    def get_image_data(self):
        """ Get the current image data.

            Returns:
            numpy array reshaped to the x,y dimensions
            specified by the xsize and ysize PVs
        """
        data = self.data_pv.get()
        x_size = self.xsize.get()
        y_size = self.ysize.get()
        return data.reshape(x_size, y_size)
