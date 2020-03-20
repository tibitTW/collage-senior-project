import numpy as np
import cv2 as cv

cap = cv.VideoCapture('src/v3.mp4')

while True:
    ret, frame = cap.read()

    if not ret: break

    cv.imshow('frame', frame)