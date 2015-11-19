from time import sleep
from monitor.camera import Camera
from monitor.plotter_pygame import PyGamePlotter


def run(plotter, camera):

    while True:
        plotter.show(camera.get_image_data())
        sleep(1.0)

if __name__ == "main":

    cam_ioc = "X1-CAM"

    plo = PyGamePlotter()
    cam = Camera(cam_ioc)

    run(plo, cam)
