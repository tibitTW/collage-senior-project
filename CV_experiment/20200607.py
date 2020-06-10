import numpy as np
import cv2 as cv
from sklearn.linear_model import LinearRegression
from time import sleep

video = cv.VideoCapture('record/videos/pr5.mp4')

hsv_color_bottom = np.array([48, 23, 44])
hsv_color_top = np.array([103, 113, 138])
line_color_bottom = np.array([102, 91, 134])
line_color_top = np.array([112, 215, 146])
glitch_bottom = np.array([149, 216, 56])
glitch_top = np.array([166, 255, 221])
while True:

    ret, frame = video.read()

    key = cv.waitKey(1)
    if key & 0xff == ord('q'):
        break

    if not ret:
        break

    frame_normalize = cv.normalize(frame, None, 0, 255, cv.NORM_MINMAX)

    hsv_image = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    glitch_mask = cv.inRange(
        hsv_image, glitch_bottom, glitch_top)

    if not np.count_nonzero(glitch_mask):

        contour_mask = cv.inRange(
            hsv_image, hsv_color_bottom, hsv_color_top)
        # get welding puddle contour
        X, Y = np.nonzero(contour_mask)
        X = X.reshape((-1, 1))
        print(X, Y)
        # line_model = LinearRegression().fit(X, Y)
        # print(line_model.coef_, line_model.intercept_)

        cv.imshow('frame', frame)
        cv.imshow('normalize', frame)
        # cv.imshow('mask', contour_mask)
        # contour_point = get_puddle_contour(contour_mask)
        # line_mask = cv.inRange(
        #     hsv_image, line_color_bottom, line_color_top)

        # pointA = (
        #     contour_point[0],
        #     contour_point[0] * line_coef + line_intercept)
        # pointB = (
        #     (contour_point[1] - line_intercept)/line_coef,
        #     contour_point[1])

        # ab_distance = ((pointA[0] - pointB[0]) ** 2 +
        #                (pointA[1] - pointB[1]) ** 2) ** 0.5

        # puddle_width = ab_distance * \
        #     line_coef / (line_coef ** 2 + 1)

        sleep(0.01)
