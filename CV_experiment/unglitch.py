import cv2 as cv
import numpy as np

video = cv.VideoCapture('./record/videos/glitch1.h264')

purple_glitch_bottom = np.array([149, 216, 56])
purple_glitch_top = np.array([166, 255, 221])


ret, frame = video.read()

while ret:

    key = cv.waitKey(1)
    if key & 0xff == ord('q'):
        break

    hsv_frame = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    glitch_mask = cv.inRange(
        hsv_frame, purple_glitch_bottom, purple_glitch_top)

    size = 0
    for row in glitch_mask:
        for point in row:
            if point:
                size = 1
                break

    if size:
        pass
    else:
        cv.imshow('frame', frame)

    ret, frame = video.read()

video.release()
cv.destroyAllWindows()
