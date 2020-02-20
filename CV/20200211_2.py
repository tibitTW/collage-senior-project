import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
from time import sleep

# size = (960, 540)
cap = cv.VideoCapture('src/v2.mp4')

# center position of cutted frame
cx, cy = 480, 270

# kernels
filter_kernel = np.ones((3, 3), np.uint8)
kernel = np.ones((3, 3), np.uint8)

# cutted size = (240, 200)
cutted_hw, cutted_hh = 260//2, 210//2

i = 0
while True:
    # get next frame
    ret, frame = cap.read()

    # break if next frame isn't exist
    if not ret: break

    # break if press key 'Q', for debug
    if cv.waitKey(1) & 0xFF == ord('q'): break

    # catch lightest part
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    ret, th = cv.threshold(gray, 240, 255, cv.THRESH_BINARY)

    cnts, _ = cv.findContours(th, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    for pic, contour in enumerate(cnts):
        area = cv.contourArea(contour)
        if area > 500:
            x, y, w, h = cv.boundingRect(contour)
            cx = x + w//2
            cy = y + h//2
            # cv.rectangle(frame, (cx - cutted_hw, cy - cutted_hh), (cx + cutted_hw, cy + cutted_hh), (255, 0, 0), 2)
            break
    
    #=======================================================================#

    cutted = frame[cy-cutted_hh : cy+cutted_hh, cx-cutted_hw : cx+cutted_hw]

    blured = cv.blur(cutted, (3, 3))

    t = [250, 430]
    edges = cv.Canny(blured, t[0], t[1])
    dilation = cv.dilate(edges, kernel, iterations = 2)

    cnts, _ = cv.findContours(dilation.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    top = np.array([])
    count = 0
    for pic, contour in enumerate(cnts):
        x, y, w, h = cv.boundingRect(contour)
        if y < 80:
            # cutted = cv.drawContours(cutted, contour, -1, (0, 255, 0), 2)
            count += 1
            top = contour
        else: cutted = cv.drawContours(cutted, contour, -1, (153, 51, 204), 2)

        if count > 1:
            top = np.vstack((top, contour))
            # sleep(5)
        i += 1

    cv.rectangle(cutted, (x, y), (x+w, y+h), (255, 255, 0), 3)
    print('銲槍高度:', x)
    cv.imshow('edges', edges)
    cv.imshow('dilation', dilation)
    cv.imshow('cutted', cutted)

    sleep(0.05)

cap.release()
cv.destroyAllWindows()