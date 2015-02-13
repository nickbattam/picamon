import unittest
import epics
from camera import Camera

__author__ = 'nick'


class CameraTest(unittest.TestCase):

    def test_xsize_reads_from_pv(self):
        cam = Camera("CAM1")
        epics.caput("CAM1:xsize", 11)

        self.assertEquals(11, cam.xsize)

    def test_ysize_reads_from_pv(self):
        cam = Camera("CAM1")
        epics.caput("CAM1:ysize", 21)

        self.assertEquals(21, cam.ysize)

    def test_get_image_data_reads_reshaped_array_from_pv(self):
        cam = Camera("CAM1")
        epics.caput("CAM1:xsize", 5)
        epics.caput("CAM1:ysize", 6)
        epics.caput("CAM1:arrayData", [1,2,3,4,5, 1,2,3,4,5,
                                       1,2,3,4,5, 1,2,3,4,5,
                                       1,2,3,4,5, 1,2,3,4,5])

        image = cam.get_image_data()
        #
        # np.array((5, 6), range(1,6))
        #
        # self.assertEquals(np.array([]), image)
