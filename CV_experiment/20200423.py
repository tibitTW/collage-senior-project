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

    frame = frame[100:700, 400:1200]
    frame = cv.rotate(frame, cv.ROTATE_180)
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    l_color = np.array([0, 255, 62])
    h_color = np.array([24, 255, 142])

    red_mask = cv.inRange(hsv, l_color, h_color)

    red = cv.bitwise_and(frame, frame, mask=red_mask)

    cnts, _ = cv.findContours(
        red_mask.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    biggest_area = 0
    biggest_cnt = np.array([])
    for pic, contour in enumerate(cnts):

        area = cv.contourArea(contour)
        if area > biggest_area:
            biggest_area = area
            biggest_cnt = contour

    if biggest_area > 1000:
        print(biggest_area)
        x, y, w, h = cv.boundingRect(biggest_cnt)
        print(x, y, w, h)
        if y < 200:
            cv.rectangle(frame, (x-3, y-3), (x+w+3, y+h+3), (255, 255, 255), 2)
            cv.circle(frame, (x+w//2, y+h//2), 3, (255, 255, 255), -1)
            cv.putText(frame, 'welding torch tip', (x+w+8, y+h//2+3),
                       cv.FONT_HERSHEY_SIMPLEX,
                       0.6, (255, 255, 255), 1, cv.LINE_AA)

    cv.imshow('frame', frame)
    # cv.imshow('red', red_mask)

    sleep(0.01)

cap.release()
cv.destroyAllWindows()
