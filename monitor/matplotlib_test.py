import epics
import matplotlib
#matplotlib.use('wx')
import matplotlib.pyplot as plt
import numpy as np

prefix = "X2-CAM"

plt.ion()
matplotlib.rcParams['toolbar'] = 'None'
mng = plt.get_current_fig_manager()
mng.resize(*mng.window.maxsize())

while True:
    try:
        data = epics.PV(prefix + ":image1:ArrayData").get()
        dimension = epics.PV(prefix + ":image1:Dimensions_RBV").get()
        array = data.reshape(dimension[0],dimension[1])

        plt.imshow(array)
        plt.draw()

    except KeyboardInterrupt:
        break


