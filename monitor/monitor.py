#!/usr/bin/python
# monitor.py
from time import sleep
from epics.pv import PV
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
        self._stop = False

        self.camera_name = PV(control_pv, callback=self.update_camera)

    def update_camera(self, value, **kw):
        """ Update the camera object linked to the monitor

            :param value: pv root for camera object
            :param kw: unused kwargs argument, required by PyEpics.
        """
        if self.camera is not None:
            self.camera.close()
        self.camera = Camera(value)
        self.set_screensize(self.camera.xsize, self.camera.ysize)

    def run(self):
        """ Refresh the image at 5Hz.

            Updates continue until stop() is signalled
        """
        while not set._stop:
            self._update_image()
            sleep(0.2)
        else:
            self._stop = False

    def stop(self):
        """ Signal the monitor to stop refreshing
        """
        self._stop = True

    def _update_image(self):
        """ Grap latest image and size data from the camera and pass to
            the plotter
        """
        if self.camera is not None:
            data = self.camera.get_image_data()
            self.plotter.show(data)