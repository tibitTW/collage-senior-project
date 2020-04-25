from picamera import PiCamera
from picamera.array import PiRGBArray
import cv2 as cv

resolution = (640, 480)


def init():
    camera = PiCamera()
    camera.resolution = resolution
    camera.brightness = 25
    rawCapture = PiRGBArray(camera, size=resolution)


def start_detect(camera, rawCapture):
    for frame in camera.capture_continuous(rawCapture, format='bgr', use_video_port=True):
        image = frame.array
        cv.imshow('frame', image)

        rawCapture.truncate(0)
