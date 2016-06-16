import epics
import numpy as np


class Camera(object):

    def set_name(self, prefix):
        self.array_pvname = prefix + ":image1:ArrayData"
        self.sizex_pvname = prefix + ":cam1:SizeX"
        self.sizey_pvname = prefix + ":cam1:SizeY"
    
    def get_data(self):

        x_size = epics.caget(self.sizex_pvname)
        y_size = epics.caget(self.sizey_pvname)

        data = epics.caget(self.array_pvname)

        reshaped = data.reshape(y_size, x_size).astype('int32')
        image_data = np.transpose(reshaped)

        return image_data

