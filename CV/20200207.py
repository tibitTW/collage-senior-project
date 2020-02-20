import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt

img = cv.imread('src/0206.png')

cutted = img[300:650, 430:930]
cutted_rgb = cv.cvtColor(cutted, cv.COLOR_BGR2RGB)
r, g, b = cv.split(cutted_rgb)

cv.imshow('R channel', r)
cv.imshow('G channel', g)

# matplotlib
plt.subplot(221), plt.imshow(cutted_rgb, 'gray'), plt.title('Original')
plt.subplot(222), plt.imshow(r, 'gray'), plt.title('R')
plt.subplot(223), plt.imshow(g, 'gray'), plt.title('G')
plt.subplot(224), plt.imshow(b, 'gray'), plt.title('B')
plt.show()

cv.waitKey(0)
cv.destroyAllWindows()