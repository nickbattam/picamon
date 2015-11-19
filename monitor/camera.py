# from pkg_resources import require
# require("numpy")

from epics import pv
import numpy as np


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
        self.data_pv = pv.PV(prefix + ":image1:ArrayData")
        self.xsize_pv = pv.PV(prefix + ":cam1:SizeX")
        self.ysize_pv = pv.PV(prefix + ":cam1:SizeY")

    def close(self):
        """ Close camerate instance, disconnecting monitors and
            callback handlers
        """
        self.data_pv.disconnect()
        self.xsize_pv.disconnect()
        self.ysize_pv.disconnect()

    @property
    def xsize(self):
        return self.xsize_pv.get()

    @property
    def ysize(self):
        return self.ysize_pv.get()

    def get_image_data(self, last_timestamp=None):
        """ Get the current image data.

            Returns:
            numpy array reshaped as (y,x) dimensions
                specified by the xsize and ysize PVs
            timestamp of data
        """
        cdata = self.data_pv.get()
        image_data = None
        timestamp = self.data_pv.timestamp
        if last_timestamp is None or timestamp > last_timestamp:
            x_size = self.xsize
            y_size = self.ysize

            data = np.array(cdata)
            reshaped = data.reshape(y_size, x_size).astype('int32')
            image_data = np.transpose(reshaped)

        return image_data, timestamp
