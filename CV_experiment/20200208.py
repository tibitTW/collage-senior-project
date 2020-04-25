import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
from time import sleep

# read video file
cap = cv.VideoCapture('src/v1.mp4')
kernel = np.ones((3, 3), np.uint8)

# define codec, create videoWriter object
fourcc = cv.VideoWriter_fourcc(*'XVID')
out = cv.VideoWriter('output.avi', fourcc, 20.0, (640, 480))

# for Canny
t1 = 250
t2 = t1 + 180

while True:

    # capture frame-by-frame
    ret, frame = cap.read()

    # exit when end
    if not ret:
        print('video end.')
        break

    edges = cv.Canny(frame, t1, t2)

    cnts, _ = cv.findContours(edges.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    for pic, contour in enumerate(cnts):
        area = cv.contourArea(contour)
        frame = cv.drawContours(frame, contour, -1, (0, 0, 255), 2)

    cv.imshow('frame', frame)
    # out.write(frame)
    sleep(0.01)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
out.release()
cv.destroyAllWindows()