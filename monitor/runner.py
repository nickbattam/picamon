import sys
from time import sleep
from camera import Camera
from plotter_pygame import PyGamePlotter


def run(plotter, camera):
    old_timestamp = -1
    while True:
        data, timestamp = camera.get_image_data()
        if timestamp != old_timestamp:
            plotter.show(data)
            old_timestamp = timestamp
        sleep(1.0)

if __name__ == "__main__":

    cam_ioc = sys.argv[1]  # "X1-CAM"

    cam = Camera(cam_ioc)
    plo = PyGamePlotter()
    plo.set_screensize(cam.xsize, cam.ysize)

    run(plo, cam)
