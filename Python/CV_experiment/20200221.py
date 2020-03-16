import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
from time import sleep

cap = cv.VideoCapture('src/v3.mp4')
w, h, _ = cap.read()[1].shape
cx, cy = 960, 540

f = open('0217_output.txt', 'a')

while True:

    ret, frame = cap.read()

    if not ret: break

    key = cv.waitKey(1)
    if key & 0xFF == ord('q'): break
    if key & 0xFF == ord('p'):
        while True:
            key = cv.waitKey(1)
            if key & 0xFF == ord('p'): break
            if key & 0xFF == ord('q'): exit()

    frame = cv.rotate(frame, cv.ROTATE_90_CLOCKWISE)

    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    ret, th = cv.threshold(gray, 180, 255, cv.THRESH_BINARY)
    
    cnts, _ = cv.findContours(th.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    for pic, contour in enumerate(cnts):
        area = cv.contourArea(contour)
        x, y, w, h = cv.boundingRect(contour)
        if area > 100:
            cx, cy = x+w//2, y+h//2
    
    cutted = frame[cy-60:cy+180, cx-110:cx+110]

    cutted_gray = cv.cvtColor(cutted, cv.COLOR_BGR2GRAY)

    _, th40 = cv.threshold(cutted_gray, 40, 255, cv.THRESH_BINARY)
    _, th50 = cv.threshold(cutted_gray, 50, 255, cv.THRESH_BINARY)
    _, th60 = cv.threshold(cutted_gray, 60, 255, cv.THRESH_BINARY)

    cnts, _ = cv.findContours(th50.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    x1, y1, x2, y2 = 220, 240, 0, 0

    for pic, contour in enumerate(cnts):
        x, y, w, h = cv.boundingRect(contour)
        if x < x1: x1 = x
        if y < y1: y1 = y
        if x+w > x2: x2 = x+w
        if y+h > y2: y2 = y+h

    merge40 = cv.merge((th40, th40, th40))
    merge50 = cv.merge((th50, th50, th50))
    merge60 = cv.merge((th60, th60, th60))

    cv.rectangle(cutted, (x1, y1), (x2, y2), (0, 0, 255), 1)
    width = x2 - x1
    if x2-x1 > 0: print('Width:', width)
    f.writelines(str(width)+'\n')

    cv.imshow('cutted', cutted)
    cv.imshow('th40', th40)
    cv.imshow('th50', th50)
    cv.imshow('th60', th60)

    sleep(0.01)

f.close()
