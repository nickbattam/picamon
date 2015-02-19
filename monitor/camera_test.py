from time import sleep
import unittest
import epics
from camera import Camera
import numpy as np

__author__ = 'nick'


class CameraTest(unittest.TestCase):

    def setUp(self):

        self.cam = Camera("CAM1")

    def test_xsize_reads_from_pv(self):

        epics.caput("CAM1:xsize", 11)

        sleep(0.1)

        self.assertEquals(11, self.cam.xsize)

    def test_ysize_reads_from_pv(self):

        epics.caput("CAM1:ysize", 21)
        sleep(0.1)

        self.assertEquals(21, self.cam.ysize)

    def test_get_image_data_reads_reshaped_array_from_pv(self):
        epics.caput("CAM1:xsize", 5)
        epics.caput("CAM1:ysize", 6)
        epics.caput("CAM1:arrayData", [1,2,3,4,5, 1,2,3,4,5,
                                       1,2,3,4,5, 1,2,3,4,5,
                                       1,2,3,4,5, 1,2,3,4,5])

        sleep(0.1)

        image = self.cam.get_image_data()

        self.assertSequenceEqual((6, 5), np.shape(image))
        np.testing.assert_array_equal(
            np.array([[1,2,3,4,5],
                      [1,2,3,4,5],
                      [1,2,3,4,5],
                      [1,2,3,4,5],
                      [1,2,3,4,5],
                      [1,2,3,4,5]]),
            image)
