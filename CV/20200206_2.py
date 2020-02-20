import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt

img = cv.imread('20200206test/frame_300.jpg')
#img.size = (960, 540)

# 抓取重點
cutted = img[350:560, 180:390]

# 色調分離
b, g, r = cv.split(cutted)
### 耗時，慎用 ###

# 取灰色
cutted_gray = cv.cvtColor(cutted, cv.COLOR_BGR2GRAY)

# 取滑鼠位置
def rtn_mouse_pos(event, x, y, flags, param):
    if event == cv.EVENT_MOUSEMOVE:
        print('Mouse at:', x, y)

cv.namedWindow('img')
cv.setMouseCallback('img', rtn_mouse_pos)

# Matplotlib
cutted = cv.cvtColor(cutted, cv.COLOR_BGR2RGB)
plt.subplot(231), plt.imshow(cutted), plt.title('original')
plt.subplot(232), plt.imshow(cutted_gray, 'gray'), plt.title('gray')
# plt.subplot(233), plt.imshow(cutted, 'gray'), plt.title('original')
plt.subplot(234), plt.imshow(r, 'gray'), plt.title('r channel')
plt.subplot(235), plt.imshow(g, 'gray'), plt.title('g channel')
plt.subplot(236), plt.imshow(b, 'gray'), plt.title('b channel')

while True:
    cv.imshow('img', img)

    plt.show()
    # cv.imshow('cutted', cutted)
    # cv.imshow('b', b)
    # cv.imshow('g', g)
    # cv.imshow('r', r)

    if cv.waitKey(1) & 0xFF == 27:
        break

cv.destroyAllWindows()

# 180, 350
# 390, 560