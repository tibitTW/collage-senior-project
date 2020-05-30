import cv2 as cv
import numpy as np
from time import sleep


def nothing(_):
    pass


src = './src/images/src3.png'

image = cv.imread(src)

image = image[300:700, 300:1100]

cv.namedWindow('Control Bars')

cv.createTrackbar('Low-H', 'Control Bars', 130, 180, nothing)
cv.createTrackbar('Low-S', 'Control Bars', 255, 255, nothing)
cv.createTrackbar('Low-V', 'Control Bars', 0, 255, nothing)
cv.createTrackbar('High-H', 'Control Bars', 180, 180, nothing)
cv.createTrackbar('High-S', 'Control Bars', 255, 255, nothing)
cv.createTrackbar('High-V', 'Control Bars', 255, 255, nothing)

while True:

    key = cv.waitKey(1)
    if key & 0xFF == ord('q'):
        break

    l_h = cv.getTrackbarPos('Low-H', 'Control Bars')
    l_s = cv.getTrackbarPos('Low-S', 'Control Bars')
    l_v = cv.getTrackbarPos('Low-V', 'Control Bars')
    h_h = cv.getTrackbarPos('High-H', 'Control Bars')
    h_s = cv.getTrackbarPos('High-S', 'Control Bars')
    h_v = cv.getTrackbarPos('High-V', 'Control Bars')

    hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)

    color_bottom = np.array([l_h, l_s, l_v])
    color_top = np.array([h_h, h_s, h_v])
    mask = cv.inRange(hsv, color_bottom, color_top)

    result = cv.bitwise_and(image, image, mask=mask)

    cv.imshow('image', image)
    cv.imshow('mask', mask)
    cv.imshow('result', result)

    print(f'color-bottom: {[l_h, l_s, l_v]}')
    print(f'color-top: {[h_h, h_s, h_v]}')

    sleep(0.1)

cv.destroyAllWindows()
