import cv2 as cv
import numpy as np
from time import sleep


def nothing(_):
    pass


src = 'Record/20200406--05_26.h264'

cap = cv.VideoCapture(src)

cv.namedWindow('Control Bars')

cv.createTrackbar('Low-H', 'Control Bars', 130, 180, nothing)
cv.createTrackbar('Low-S', 'Control Bars', 255, 255, nothing)
cv.createTrackbar('Low-V', 'Control Bars', 0, 255, nothing)
cv.createTrackbar('High-H', 'Control Bars', 180, 180, nothing)
cv.createTrackbar('High-S', 'Control Bars', 255, 255, nothing)
cv.createTrackbar('High-V', 'Control Bars', 255, 255, nothing)

while True:
    ret, frame = cap.read()

    if not ret:
        break

    key = cv.waitKey(1)
    if key & 0xFF == ord('q'):
        break

    if key & 0xFF == ord('p'):
        while True:
            key = cv.waitKey(1)
            if key & 0xFF == ord('p'):
                break
            if key & 0xFF == ord('q'):
                exit()

    l_h = cv.getTrackbarPos('Low-H', 'Control Bars')
    l_s = cv.getTrackbarPos('Low-S', 'Control Bars')
    l_v = cv.getTrackbarPos('Low-V', 'Control Bars')
    h_h = cv.getTrackbarPos('High-H', 'Control Bars')
    h_s = cv.getTrackbarPos('High-S', 'Control Bars')
    h_v = cv.getTrackbarPos('High-V', 'Control Bars')

    # frame = frame[100:-100, 300:-300]

    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    color_bottom = np.array([l_h, l_s, l_v])
    color_top = np.array([h_h, h_s, h_v])
    mask = cv.inRange(hsv, color_bottom, color_top)

    result = cv.bitwise_and(frame, frame, mask=mask)

    cv.imshow('frame', frame)
    cv.imshow('mask', mask)
    cv.imshow('result', result)

    print(f'color-bottom: {[l_h, l_s, l_v]}')
    print(f'color-top: {[h_h, h_s, h_v]}')

    sleep(0.1)

cap.release()
cv.destroyAllWindows()
