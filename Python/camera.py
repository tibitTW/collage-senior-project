from picamera import PiCamera
from picamera.array import PiRGBArray
import cv2 as cv

resolution = (640, 480)


def init():
    camera = PiCamera()
    camera.resolution = resolution
    rawCapture = PiRGBArray(camera, size=resolution)


def stream(camera, rawCapture):
    for frame in camera.capture_continuous(rawCapture, format='bgr', use_video_port=True):
        image = frame.array
        cv.imshow('frame', image)

        rawCapture.truncate(0)

        key = cv.waitKey(1) & 0xFF
        if key == ord('q'):
            break
