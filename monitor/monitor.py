#!/usr/bin/python
# monitor.py
from time import sleep

import numpy as np
import epics
from epics import pv

from camera import Camera


class Monitor(object):
    """ monitor class to listen for broadcast instructions
        from network with pv name and camera to stream from
    """

    def __init__(self, control_pv, plotter):
        """
            Arguments:
                control_pv -- name of PV containing target camera data for this monitor (e.g. MON-CONTROL:PIx)
                plotter -- image rendering tool
        """
        self.camera = None
        self.plotter = plotter

        self.camera_name = pv.PV(
            control_pv,
            callback=self.update_camera)

    def update_camera(self, value, **kw):
        if self.camera is not None:
            self.camera.close()
        self.camera = Camera(value)

    def run(self):

        while True:
            self._update_image()
            sleep(0.2)

    def _update_image(self):
        """ Grap latest image and size data from the camera and pass to
            the plotter
        """
        if self.camera is not None:
            data = self.camera.get_image_data()
            self.plotter.show(data,
                              self.camera.xsize,
                              self.camera.ysize)