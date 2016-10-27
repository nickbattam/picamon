import epics
import numpy as np


class Camera(object):

    DATA_RECORD = ":image1:ArrayData"
    XSIZE_RECORD = ":cam1:SizeX"
    YSIZE_RECORD = ":cam1:SizeY"

    def __init__(self):
        self._prefix = ""

    def update_name(self, prefix):
        if prefix is not None and prefix != self._prefix:
            self._prefix = prefix
            self.array_pvname = prefix + Camera.DATA_RECORD
            self.sizex_pvname = prefix + Camera.XSIZE_RECORD
            self.sizey_pvname = prefix + Camera.YSIZE_RECORD

    def has_feed(self):
        return bool(self._prefix)

    @property
    def name(self):
        return self._prefix

    def get_data(self):

        x_size = epics.caget(self.sizex_pvname)
        y_size = epics.caget(self.sizey_pvname)

        data = epics.caget(self.array_pvname)

        reshaped = data.reshape(y_size, x_size).astype('int32')
        image_data = np.transpose(reshaped)

        return image_data

