import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from time import sleep

cap = cv.VideoCapture('src/20200417.mp4')

while True:

    ret, frame = cap.read()

    if not ret:
        print('Video end.')
        break
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

    frame = frame[300:800, 300:1200]
    # gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    # ret, th1 = cv.threshold(frame, 127, 255, cv.THRESH_BINARY)
    b, g, r = cv.split(frame)
    # cv.imshow('th1', th1)
    cv.imshow('r', r)
    cv.imshow('g', g)
    cv.imshow('b', b)
    cv.imshow('frame', frame)

    sleep(0.01)

cap.release()
cv.destroyAllWindows()
