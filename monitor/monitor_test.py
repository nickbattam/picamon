#!/usr/bin/python

import unittest
from mock import patch, MagicMock, PropertyMock

from monitor import Monitor


class MonitorUpdateTest(unittest.TestCase):

    def setUp(self):
        with patch('monitor.pv.PV'):
            mock_plotter = MagicMock()
            self.monitor = Monitor("MYNAME", mock_plotter)

    def test_does_nothing_if_camera_is_None(self):
        self.monitor.camera = None

        try:
            self.monitor._update_image()
            self.assertTrue(True)
        except Exception as ex:
            self.fail("Unexpected expection thrown" + str(ex))


    def test_gets_image_data_from_camera_when_not_None(self):
        mock_camera = MagicMock()
        self.monitor.camera = mock_camera

        self.monitor._update_image()

        mock_camera.get_image_data.assert_called_once_with()

    def test_get_size_data_from_camera_when_not_None(self):
        mock_camera = MagicMock()

        mock_xsize = PropertyMock(return_value=100)
        mock_ysize = PropertyMock(return_value=200)
        type(mock_camera).xsize = mock_xsize
        type(mock_camera).ysize = mock_ysize

        self.monitor.camera = mock_camera

        self.monitor._update_image()

        mock_xsize.assert_called_once_with()
        mock_ysize.assert_called_once_with()

    def test_calls_plotter_with_image_and_size_data(self):
        data = 111
        xsize = 100
        ysize = 200
        mock_camera = MagicMock(xsize=xsize, ysize=ysize)
        mock_camera.get_image_data = MagicMock(return_value=data)
        self.monitor.camera = mock_camera

        self.monitor._update_image()

        self.monitor.plotter.show.assert_called_once_with(data, xsize, ysize)


if __name__ == '__main__':
    unittest.main()
